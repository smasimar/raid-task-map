"""
Reads the Escape from Tarkov log files and follows the state of the game:
game mode, raid loading / starting / in progress / ended, and task messages.

The log patterns and the raid state logic are ported from TarkovMonitor
(https://github.com/the-hideout/TarkovMonitor, GameWatcher.cs), which is
licensed under GPL-3.0. Copyright (c) the TarkovMonitor contributors.

Only log files are read. Nothing here touches the game process.
"""

import json
import os
import re
import time

# "2026-11-14 20:15:47.776|1.3.0.2.48779|Info|application|GameStarted:..." (the time zone is optional)
LINE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})\.(\d{3})(?: [+-]\d{2}:\d{2})?\|(.*)$")
MODE_RE = re.compile(r"Session mode: ([^\s|]+)")
PROFILE_RE = re.compile(r"(?:Select(?:ed)?Profile|PrepareSelectedProfileLocally) ProfileId:(\w+)")
STATUS_PROFILE_RE = re.compile(r"Profileid: (\w+)")
INSURANCE_REQUEST = "/client/insurance/items/list/cost"   # the insurance screen, which only a PMC gets before a raid
PMC_COUNTDOWN_SECONDS = 3.0   # a PMC raid has a countdown between GameStarting and GameStarted; a Scav raid has none
SCENE_RE = re.compile(r"scene preset path:(maps/[a-zA-Z0-9_]+\.bundle)")
LOCATION_RE = re.compile(r"Location: ([^,]+)")
RAID_ID_RE = re.compile(r"shortId: ([A-Z0-9]{6})")
# Transits. At the start of each map the game writes "[Transit] Flag:Common, RaidId:<id>, Count:<n>, Locations:a -> b -> "
# (PvP: "[Transit] `<profile>` Count:<n>, ..."). The raid id stays the same through the transits and Count is the
# number of transits so far. Before a PvE transit it also writes "PVE transit hop ... side:Pmc".
# Before a transit to an online map (Ground Zero 21+ -> Streets in PvE) it writes "Transit reconnect status:..."
# before the map loads, and the [Transit] line comes only after GameStarted.
TRANSIT_RECONNECT = "application|Transit reconnect "
TRANSIT_RE = re.compile(r"\[Transit\].*?(?:RaidId:(\w+), )?Count:(\d+)")
HOP_SIDE_RE = re.compile(r"transit hop .*?side:(\w+)", re.I)
LOG_FOLDER_RE = re.compile(r"^log_\d+\.\d+\.\d+_\d+-\d+-\d+")

SESSION_MODES = {
    "pve": "pve",
    "regular": "regular", "pvp": "regular",
    "pvpseason": "pvp-season", "seasonal": "pvp-season", "szn": "pvp-season",
}
TASK_STATUS = {10: "started", 11: "failed", 12: "finished"}

# A raid left open by a game crash is not kept for ever.
MAX_RAID_SECONDS = 90 * 60
MAX_LOADING_SECONDS = 15 * 60

UNINSTALL_KEYS = (
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\EscapeFromTarkov",
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\EscapeFromTarkov",
    r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 3932890",
    r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Steam App 3932890",
)


def install_locations():
    """Game folders named in the Windows registry (launcher and Steam installs)."""
    found = []
    if os.name != "nt":
        return found
    try:
        import winreg
    except ImportError:
        return found
    for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
        for view in (winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY):
            for key in UNINSTALL_KEYS:
                try:
                    with winreg.OpenKey(hive, key, 0, winreg.KEY_READ | view) as k:
                        value = str(winreg.QueryValueEx(k, "InstallLocation")[0]).strip()
                except OSError:
                    continue
                if value and value not in found:
                    found.append(value)
    return found


def default_logs_dir() -> str:
    for root in install_locations():
        for sub in ("Logs", os.path.join("build", "Logs")):
            p = os.path.join(root, sub)
            if os.path.isdir(p):
                return p
    return ""


def log_folders(logs_dir: str):
    """The session folders, Logs/log_<date>_<time>_<version>, oldest first."""
    try:
        names = [n for n in os.listdir(logs_dir) if LOG_FOLDER_RE.match(n) and os.path.isdir(os.path.join(logs_dir, n))]
    except OSError:
        return []
    # the hour has one or two digits ("9-03-18"), so the names do not sort as text
    names.sort(key=lambda n: [int(x) for x in re.findall(r"\d+", n)])
    return [os.path.join(logs_dir, n) for n in names]


def newest_log_folder(logs_dir: str):
    """The folder of the latest game session."""
    folders = log_folders(logs_dir)
    return folders[-1] if folders else None


def task_events(logs_dir: str, after: float = 0.0):
    """The task messages of all sessions later than `after`, oldest first.
    Each is {"type": "task", "status", "id", "time", "mode"}."""
    out = []
    for folder in log_folders(logs_dir):
        state = GameState()
        # the mode is in one file and the task messages in the other: put them in time order
        for entry in sorted(LogFollower(folder).read(), key=lambda e: e[0]):
            out += [ev for ev in state.handle(*entry) if ev["type"] == "task" and ev["time"] > after]
    out.sort(key=lambda ev: ev["time"])
    return out


def net_task_changes(events):
    """The last status of each task, as {mode: {"started": [ids], "ended": [ids]}}."""
    last = {}
    for ev in events:
        last[(ev["mode"], ev["id"])] = ev["status"]
    out = {}
    for (mode, task_id), status in last.items():
        out.setdefault(mode, {"started": [], "ended": []})["started" if status == "started" else "ended"].append(task_id)
    return out


def entry_time(date: str, clock: str, millis: str) -> float:
    """Log times are local time."""
    try:
        return time.mktime(time.strptime(f"{date} {clock}", "%Y-%m-%d %H:%M:%S")) + int(millis) / 1000.0
    except (ValueError, OverflowError):
        return 0.0


class EntryReader:
    """Turns raw log bytes into entries: (time, message, json or None).

    An entry is one dated line. A notification entry is followed by a JSON
    block on the next lines. Data can arrive cut at any byte, so an entry is
    given out only when it is complete.
    """

    def __init__(self):
        self.rest = b""       # bytes after the last full line
        self.pending = None   # [time, message, [body lines]]

    def feed(self, data: bytes):
        data = self.rest + data
        cut = data.rfind(b"\n")
        if cut < 0:
            self.rest = data
            return []
        self.rest = data[cut + 1:]
        out = []
        for line in data[:cut].decode("utf-8", "replace").split("\n"):
            line = line.rstrip("\r")
            m = LINE_RE.match(line)
            if m:
                self._flush(out)
                self.pending = [entry_time(m.group(1), m.group(2), m.group(3)), m.group(4), []]
            elif self.pending is not None and line.strip():
                self.pending[2].append(line)
        # a notification is complete when its JSON block is closed; other lines have no block
        if self.pending is not None:
            body = self.pending[2]
            if "Got notification" not in self.pending[1] or (body and body[-1] == "}"):
                self._flush(out)
        return out

    def _flush(self, out):
        if self.pending is None:
            return
        when, message, body = self.pending
        self.pending = None
        data = None
        if body and body[0].startswith("{"):
            try:
                data = json.loads("\n".join(body))
            except ValueError:
                data = None
        out.append((when, message, data))


def new_raid():
    return {"phase": "idle", "scenePath": None, "location": None, "online": None,
            "raidId": None, "since": 0.0, "started": None, "side": None, "transits": 0}


class GameState:
    """Follows the game through its log entries.

    raid["phase"] is one of:
      idle      not in a raid
      loading   the map loads, or the game looks for a match
      starting  the countdown before the raid
      raid      the raid is in progress; raid["started"] is its start time

    raid["side"] is "pmc" or "scav", or None when the logs do not tell.
    """

    def __init__(self):
        self.mode = None
        self.raid = new_raid()
        self.started_by_id = {}   # raid id -> start time, to keep the timer after a reconnect
        self.side_by_id = {}      # raid id -> side, for the same reason
        self.profile_id = None    # the PMC profile, from the profile lines in the menus
        self._status_profile = None   # the profile that is in the raid
        self._starting = None         # time of GameStarting
        self._backend_seen = False    # the backend log is there, so the insurance rule can be used
        self._insured = False         # the game asked for the insurance cost since the last raid
        self._transit = None          # (raid id or None, count) from the [Transit] line of the raid that loads
        self._hop_side = None         # the side from the "transit hop" line before a transit
        self._last_side = None        # the side of the last raid, for a transit with no other side data
        self.side_by_transit = {}     # transit raid id -> side of the first map
        self._reconnect = False       # a "Transit reconnect" line came before the map that loads
        self._side_before = None      # the side of the raid before the one that is in progress

    def snapshot(self):
        return {"mode": self.mode, "raid": dict(self.raid)}

    def expire(self, now: float) -> bool:
        """Close a raid that never got an end line (game crash). True if it changed."""
        r = self.raid
        limit = MAX_RAID_SECONDS if r["phase"] == "raid" else MAX_LOADING_SECONDS
        start = r["started"] if r["phase"] == "raid" else r["since"]
        if r["phase"] != "idle" and now - (start or 0) > limit:
            self.raid = new_raid()
            return True
        return False

    def _transit_side(self):
        """The side of a raid that comes from a transit: the same as on the map before.
        No insurance screen comes before a transit, and the game selects the profile again
        (as at the end of a raid), so the other rules would see a Scav raid."""
        if self._reconnect:
            return self._hop_side or self._last_side
        if not self._transit or self._transit[1] < 1:
            return None
        return self._hop_side or self.side_by_transit.get(self._transit[0]) or self._last_side

    def _side(self, started: float):
        """PMC or Scav.

        1. Before a PMC raid the game shows the insurance screen and asks its server for the
           cost; before a Scav raid it does not. This works for local and online raids.
           (Found in real logs: 30 PMC raids all had the request, the Scav raid had none.)
        2. Without the backend log, for an online raid: a Scav raid uses a different profile
           than the one selected in the menus; or, if the profiles are not known, only a PMC
           raid has a countdown (the same rule as TarkovMonitor).
        """
        if self._backend_seen:
            return "pmc" if self._insured else "scav"
        if not self.raid["online"]:
            return None
        if self._status_profile and self.profile_id:
            return "pmc" if self._status_profile == self.profile_id else "scav"
        countdown = started - self._starting if self._starting else 0.0
        return "pmc" if countdown > PMC_COUNTDOWN_SECONDS else "scav"

    def handle(self, when: float, message: str, data):
        """Apply one log entry. Returns a list of events (possibly empty):
        {"type": "game"} when the mode or the raid changed,
        {"type": "task", "status": "started|failed|finished", "id": ...}."""
        before = (self.mode, dict(self.raid))
        events = []
        r = self.raid

        if "|backend|" in message:
            self._backend_seen = True
            if "---> Request" in message and INSURANCE_REQUEST in message:
                self._insured = True
        elif "Session mode: " in message:
            m = MODE_RE.search(message)
            if m:
                self.mode = SESSION_MODES.get(m.group(1).lower())
        elif PROFILE_RE.search(message):
            self.profile_id = PROFILE_RE.search(message).group(1)
            # the profile is selected again when the game goes back to the menus:
            # this is the only end mark of a local (PvE) raid
            if r["phase"] != "idle" and when >= r["since"]:
                self.raid = new_raid()
        elif "application|scene preset path:" in message:
            self.raid = r = new_raid()
            self._status_profile = self._starting = self._transit = None
            r["phase"] = "loading"
            r["since"] = when
            m = SCENE_RE.search(message)
            if m:
                r["scenePath"] = m.group(1)
        elif "application|TRACE-NetworkGameCreate profileStatus" in message:
            m = LOCATION_RE.search(message)
            if m:
                r["location"] = m.group(1).strip()
            r["online"] = "RaidMode: Online" in message
            m = STATUS_PROFILE_RE.search(message)
            self._status_profile = m.group(1) if m else None
            m = RAID_ID_RE.search(message)
            if m:
                r["raidId"] = m.group(1)
            if r["phase"] == "idle":
                r["phase"] = "loading"
                r["since"] = when
        elif "application|GameStarting" in message:
            self._starting = when
            if r["phase"] in ("idle", "loading"):
                if r["phase"] == "idle":
                    r["since"] = when
                r["phase"] = "starting"
        elif "application|GameStarted" in message:
            if r["phase"] == "idle":
                r["since"] = when
            r["phase"] = "raid"
            # a reconnect to the same raid keeps the first start time
            r["started"] = self.started_by_id.get(r["raidId"], when) if r["raidId"] else when
            if r["raidId"]:
                self.started_by_id[r["raidId"]] = r["started"]
            r["side"] = self.side_by_id.get(r["raidId"]) or self._transit_side() or self._side(when)
            r["transits"] = self._transit[1] if self._transit else 0
            if r["raidId"] and r["side"]:
                self.side_by_id[r["raidId"]] = r["side"]
            if self._transit and self._transit[0] and r["side"] and self._transit[1] == 0:
                self.side_by_transit[self._transit[0]] = r["side"]
            self._side_before = self._last_side
            if r["side"]:
                self._last_side = r["side"]
            self._hop_side = None
            self._reconnect = False
        elif TRANSIT_RECONNECT in message:
            self._reconnect = True
        elif HOP_SIDE_RE.search(message):
            side = HOP_SIDE_RE.search(message).group(1).lower()
            self._hop_side = "pmc" if side.startswith("pmc") else "scav"
        elif "application|[Transit]" in message and TRANSIT_RE.search(message):
            m = TRANSIT_RE.search(message)
            self._transit = (m.group(1), int(m.group(2)))
            if self._transit[1] == 0:
                self._hop_side = None   # a new raid, not a transit
            elif r["phase"] == "raid" and not r["transits"]:
                # the line came after GameStarted (transit to an online map): the raid is a transit
                # from the raid before, so it has the side of that raid
                r["transits"] = self._transit[1]
                side = self._hop_side or self.side_by_transit.get(self._transit[0]) or self._side_before
                if side and side != r["side"]:
                    r["side"] = self._last_side = side
                    if r["raidId"]:
                        self.side_by_id[r["raidId"]] = side
        elif ("application|Network game matching aborted" in message
              or "application|Network game matching cancelled" in message):
            self.raid = new_raid()
        elif "Got notification | UserMatchOver" in message:
            # the two log files are read one after the other, so an end line can be older than the raid
            if r["phase"] != "idle" and when >= r["since"]:
                self.raid = new_raid()
        elif "Got notification | ChatMessageReceived" in message and isinstance(data, dict):
            msg = data.get("message") if isinstance(data.get("message"), dict) else {}
            status = TASK_STATUS.get(msg.get("type"))
            task_id = str(msg.get("templateId") or "").split(" ")[0]
            if status and task_id:
                events.append({"type": "task", "status": status, "id": task_id, "time": when, "mode": self.mode})

        if before[1]["phase"] != "idle" and self.raid["phase"] == "idle":
            self._insured = False   # the next raid needs its own insurance request
        if before != (self.mode, self.raid):
            events.append({"type": "game"})
        return events


class LogFollower:
    """Reads the new bytes of the application, notification and backend logs of one session folder."""

    KINDS = ("application", "notifications", "backend")

    def __init__(self, folder: str):
        self.folder = folder
        self.offsets = {}                 # file path -> bytes read
        self.readers = {k: EntryReader() for k in self.KINDS}

    def _files(self, kind: str):
        try:
            names = sorted(n for n in os.listdir(self.folder) if n.lower().endswith(".log") and kind in n.lower())
        except OSError:
            return []
        return [os.path.join(self.folder, n) for n in names]

    def read(self):
        """All complete new entries of the three logs, in time order."""
        entries = []
        for kind in self.KINDS:
            for path in self._files(kind):
                done = self.offsets.get(path, 0)
                try:
                    if os.path.getsize(path) <= done:
                        continue
                    with open(path, "rb") as f:
                        f.seek(done)
                        data = f.read()
                except OSError:
                    continue
                self.offsets[path] = done + len(data)
                entries.extend(self.readers[kind].feed(data))
        entries.sort(key=lambda e: e[0])   # stable: lines with the same time keep the order of their file
        return entries

