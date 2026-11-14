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
PROFILE_RE = re.compile(r"(?:Select(?:ed)?Profile|PrepareSelectedProfileLocally) ProfileId:\w+")
SCENE_RE = re.compile(r"scene preset path:(maps/[a-zA-Z0-9_]+\.bundle)")
LOCATION_RE = re.compile(r"Location: ([^,]+)")
RAID_ID_RE = re.compile(r"shortId: ([A-Z0-9]{6})")
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
            "raidId": None, "since": 0.0, "started": None}


class GameState:
    """Follows the game through its log entries.

    raid["phase"] is one of:
      idle      not in a raid
      loading   the map loads, or the game looks for a match
      starting  the countdown before the raid
      raid      the raid is in progress; raid["started"] is its start time
    """

    def __init__(self):
        self.mode = None
        self.raid = new_raid()
        self.started_by_id = {}   # raid id -> start time, to keep the timer after a reconnect

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

    def handle(self, when: float, message: str, data):
        """Apply one log entry. Returns a list of events (possibly empty):
        {"type": "game"} when the mode or the raid changed,
        {"type": "task", "status": "started|failed|finished", "id": ...}."""
        before = (self.mode, dict(self.raid))
        events = []
        r = self.raid

        if "Session mode: " in message:
            m = MODE_RE.search(message)
            if m:
                self.mode = SESSION_MODES.get(m.group(1).lower())
        elif PROFILE_RE.search(message):
            # the profile is selected again when the game goes back to the menus:
            # this is the only end mark of a local (PvE) raid
            if r["phase"] != "idle" and when >= r["since"]:
                self.raid = new_raid()
        elif "application|scene preset path:" in message:
            self.raid = r = new_raid()
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
            m = RAID_ID_RE.search(message)
            if m:
                r["raidId"] = m.group(1)
            if r["phase"] == "idle":
                r["phase"] = "loading"
                r["since"] = when
        elif "application|GameStarting" in message:
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

        if before != (self.mode, self.raid):
            events.append({"type": "game"})
        return events


class LogFollower:
    """Reads the new bytes of the application and notification logs of one session folder."""

    KINDS = ("application", "notifications")

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
        """All complete new entries, the application log first."""
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
        return entries

