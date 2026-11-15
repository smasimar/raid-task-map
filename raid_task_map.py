#!/usr/bin/env python3
"""
Raid Task Map - a local task map and task tracker for Escape from Tarkov.

What it does
  * Serves a map page at http://localhost:3000
  * Reads your progress from TarkovTracker.org (api.tarkovtracker.org) with your API token,
    and sends your changes there when you set that on
  * Watches the EFT screenshots folder: every new screenshot moves your marker on the map
  * Reads the game's log files: raid map and timer, tasks started, completed and failed

Only the Python standard library is used. Run:  python raid_task_map.py

Copyright (C) 2026 the Raid Task Map contributors.
This program is free software: you can redistribute it and/or modify it under the terms of
the GNU General Public License, version 3, as published by the Free Software Foundation.
It comes with no warranty. See the LICENSE file.

Not affiliated with or approved by Battlestate Games.
"""
import json
import os
import queue
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import game_logs


def _arg(name: str, default: str) -> str:
    """The value after a command-line option, for example: --port 3005"""
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv[1:-1] else default


APP_NAME = "Raid Task Map"
APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = Path(_arg("--config", str(APP_DIR / "config.json")))
STATE_PATH = Path(_arg("--state", str(APP_DIR / "state.json")))  # a different file for tests
GAME_MODES = ("regular", "pve", "pvp-season")
PORT =int(_arg("--port", os.environ.get("RTM_PORT") or os.environ.get("TQM_PORT") or "3000"))
TT_API = _arg("--tracker", "https://api.tarkovtracker.org")  # a local stand-in for tests
USER_AGENT = "RaidTaskMap/1.0 (local)"

PROGRESS_MIN_AGE = 60   # seconds a cached /progress answer is reused (protects the daily quota)
PROGRESS_FORCE_AGE = 5  # same, when the page asks for a forced reload
ALLOWED_HOSTS = {"localhost", "127.0.0.1", "[::1]"}

# Based on TarkovMonitor's patterns, but any screenshot number "(12)" and
# exponent-form quaternion parts "1E-05" are accepted too.
_Q = r"-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
SCREENSHOT_RE = re.compile(r"\d{4}-\d{2}-\d{2}\[\d{2}-\d{2}\]_?(?P<position>.+) \(\d+\)\.png$")
POSITION_RE = re.compile(
    r"(?P<x>-?[\d]+\.[\d]{2}), (?P<y>-?[\d]+\.[\d]{2}), (?P<z>-?[\d]+\.[\d]{2})_?"
    rf"(?P<rx>{_Q}), (?P<ry>{_Q}), (?P<rz>{_Q}), (?P<rw>{_Q})"
)


# --------------------------------------------------------------------------- config

def documents_dir() -> Path:
    """The real Documents folder (handles OneDrive redirection on Windows)."""
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            # CSIDL_PERSONAL = 5
            if ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf) == 0 and buf.value:
                return Path(buf.value)
        except Exception:
            pass
    return Path.home() / "Documents"


def default_screenshots_dir() -> str:
    return str(documents_dir() / "Escape From Tarkov" / "Screenshots")



def load_config() -> dict:
    cfg = {"tokens": {}, "mode": "", "screenshotsDir": "", "deleteScreenshots": False, "logsDir": "",
           "autoTick": True, "writeTT": False}
    if CONFIG_PATH.exists():
        try:
            cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
        except Exception as exc:
            print(f"[config] could not read config.json: {exc}")
    if not cfg.get("screenshotsDir"):
        cfg["screenshotsDir"] = default_screenshots_dir()
    if not isinstance(cfg.get("tokens"), dict):
        cfg["tokens"] = {}
    old = cfg.pop("token", "")  # earlier versions kept one token
    if old:
        cfg["tokens"].setdefault(game_mode_for_token(old), old)
    return cfg


def save_json(path: Path, obj: dict) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    os.replace(tmp, path)


def save_config(cfg: dict) -> None:
    save_json(CONFIG_PATH, cfg)


def game_mode_for_token(token: str) -> str:
    """json.tarkov.dev game mode that matches the TarkovTracker token prefix."""
    t = (token or "").upper()
    if t.startswith("PVE_"):
        return "pve"
    if t.startswith("SZN_"):
        return "pvp-season"
    return "regular"


CONFIG = load_config()
CONFIG_LOCK = threading.Lock()


def active_mode() -> str:
    """The game mode the app shows: the last one set, if it has a token; else a mode that has one."""
    with CONFIG_LOCK:
        tokens = CONFIG["tokens"]
        if CONFIG.get("mode") in tokens:
            return CONFIG["mode"]
        return next((m for m in GAME_MODES if m in tokens), "regular")


def token_for(mode: str) -> str:
    with CONFIG_LOCK:
        return CONFIG["tokens"].get(mode, "")


def use_game_mode(mode: str) -> bool:
    """The game runs in this mode: show it, if there is a token for it. True if the mode changed."""
    if not mode or mode == active_mode() or not token_for(mode):
        return False
    with CONFIG_LOCK:
        CONFIG["mode"] = mode
        save_config(CONFIG)
    return True


# --------------------------------------------------------------------------- events

class EventHub:
    def __init__(self):
        self.clients = []
        self.lock = threading.Lock()
        self.state = {"position": None, "game": None}

    def subscribe(self):
        q = queue.Queue(maxsize=100)
        with self.lock:
            self.clients.append(q)
        return q

    def unsubscribe(self, q):
        with self.lock:
            if q in self.clients:
                self.clients.remove(q)

    def publish(self, event: dict):
        if event.get("type") == "position":
            self.state["position"] = event
        if event.get("type") == "game":
            self.state["game"] = event
        with self.lock:
            for q in list(self.clients):
                try:
                    q.put_nowait(event)
                except queue.Full:
                    pass


HUB = EventHub()


# --------------------------------------------------------------------------- task list

class QuestList:
    """The tasks you have in the game, for each game mode. Kept in state.json.

    selected: task ids. custom: names of tasks that are not in the tarkov.dev data.
    logTime: the time of the last task message from the game logs that was applied,
    so a restart does not apply the same messages again.
    """

    def __init__(self, path: Path, publish=None):
        self.path = path
        self.publish = publish or (lambda event: None)
        self.lock = threading.Lock()
        self.data = {"modes": {}, "migrated": [], "logTime": 0.0, "writes": {}}
        self.changed = 0.0   # time of the last queued write
        if path.exists():
            try:
                self.data.update(json.loads(path.read_text(encoding="utf-8")))
            except Exception as exc:
                print(f"[tasks] could not read {path.name}: {exc}")

    def _mode(self, mode: str) -> dict:
        return self.data["modes"].setdefault(mode, {"selected": [], "custom": []})

    def public(self) -> dict:
        with self.lock:
            return {"modes": json.loads(json.dumps(self.data["modes"])), "migrated": list(self.data["migrated"])}

    def apply(self, mode, add=(), remove=(), add_custom=(), remove_custom=(), migrated=False, log_time=None, note=None):
        """Change the list of one mode, save it, and tell the open pages."""
        with self.lock:
            m = self._mode(mode)
            before = json.dumps(m)
            gone = set(remove)
            m["selected"] = ([x for x in m["selected"] if x not in gone]
                             + [x for x in dict.fromkeys(add) if x not in m["selected"] and x not in gone])
            low = {n.lower() for n in remove_custom}
            m["custom"] = [n for n in m["custom"] if n.lower() not in low]
            for name in add_custom:
                if name.lower() not in {n.lower() for n in m["custom"]}:
                    m["custom"].append(name)
            if migrated and mode not in self.data["migrated"]:
                self.data["migrated"].append(mode)
            if log_time is not None:
                self.data["logTime"] = max(float(self.data.get("logTime") or 0), log_time)
            save_json(self.path, self.data)
            changed = before != json.dumps(m)
            event = {"type": "quests", "mode": mode, "selected": list(m["selected"]), "custom": list(m["custom"])}
        if note:
            event["note"] = note
        if changed or note:
            self.publish(event)
        return event

    # -- progress changes that wait to be sent to TarkovTracker
    def _writes(self, mode: str) -> dict:
        return self.data["writes"].setdefault(mode, {"tasks": {}, "objectives": {}})

    def queue_task(self, mode: str, task_id: str, state: str):
        with self.lock:
            self._writes(mode)["tasks"][task_id] = state
            self.changed = time.time()
            save_json(self.path, self.data)

    def queue_objective(self, mode: str, objective_id: str, patch: dict):
        """Several changes to one objective become one write with the last values."""
        with self.lock:
            self._writes(mode)["objectives"].setdefault(objective_id, {}).update(patch)
            self.changed = time.time()
            save_json(self.path, self.data)

    def pending(self, mode: str = None) -> dict:
        with self.lock:
            w = self.data["writes"]
            copy = json.loads(json.dumps(w))
        return copy.get(mode, {"tasks": {}, "objectives": {}}) if mode else copy

    def pending_count(self) -> int:
        with self.lock:
            return sum(len(w["tasks"]) + len(w["objectives"]) for w in self.data["writes"].values())

    def sent(self, mode: str, kind: str, item_id: str, value):
        """Remove a write that was sent, unless it changed again in the meantime."""
        with self.lock:
            items = self._writes(mode)[kind]
            if items.get(item_id) == value:
                del items[item_id]
                save_json(self.path, self.data)

    def log_time(self) -> float:
        with self.lock:
            return float(self.data.get("logTime") or 0)

    def apply_task_event(self, ev: dict, fallback_mode: str):
        """A task message from the game logs: started = tick, finished or failed = untick."""
        mode = ev.get("mode") or fallback_mode
        note = {"status": ev["status"], "id": ev["id"]}
        if ev["status"] == "started":
            return self.apply(mode, add=[ev["id"]], log_time=ev["time"], note=note)
        return self.apply(mode, remove=[ev["id"]], log_time=ev["time"], note=note)


def overlay_progress(body: bytes, pending: dict) -> bytes:
    """A /progress answer with the changes that are not sent yet put on top,
    so the page shows a click at once and keeps it after a reload."""
    if not pending["tasks"] and not pending["objectives"]:
        return body
    try:
        doc = json.loads(body)
        data = doc["data"]
    except (ValueError, KeyError, TypeError):
        return body

    def entry(key, item_id):
        rows = data.setdefault(key, [])
        row = next((r for r in rows if r.get("id") == item_id), None)
        if row is None:
            row = {"id": item_id}
            rows.append(row)
        return row

    for task_id, state in pending["tasks"].items():
        entry("tasksProgress", task_id).update({"complete": state == "completed", "failed": state == "failed"})
    for objective_id, patch in pending["objectives"].items():
        row = entry("taskObjectivesProgress", objective_id)
        if "state" in patch:
            row["complete"] = patch["state"] == "completed"
        if "count" in patch:
            row["count"] = patch["count"]
    return json.dumps(doc).encode("utf-8")


QUESTS = QuestList(STATE_PATH, HUB.publish)


def quaternion_to_yaw(x, z, y, w):
    """Same conversion TarkovMonitor uses (note the swapped argument names)."""
    import math
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.degrees(math.atan2(siny_cosp, cosy_cosp))


def parse_screenshot(filename: str):
    m = SCREENSHOT_RE.search(filename)
    if not m:
        return None
    p = POSITION_RE.search(m.group("position"))
    if not p:
        return None
    g = {k: float(v) for k, v in p.groupdict().items()}
    return {
        "x": g["x"], "y": g["y"], "z": g["z"],
        "rotation": quaternion_to_yaw(g["rx"], g["ry"], g["rz"], g["rw"]),
    }


# --------------------------------------------------------------------------- watchers

def screenshot_watcher():
    seen = set()
    current_dir = None
    while True:
        with CONFIG_LOCK:
            folder = CONFIG.get("screenshotsDir") or ""
            delete_after = bool(CONFIG.get("deleteScreenshots"))
        try:
            d = Path(folder)
            if folder and d.is_dir():
                names = {n for n in os.listdir(d) if n.lower().endswith(".png")}
                if current_dir != folder:
                    # first scan of this folder: existing files are history, not new positions
                    seen = names
                    current_dir = folder
                    print(f"[screenshots] watching {folder}")
                else:
                    for name in sorted(names - seen):
                        pos = parse_screenshot(name)
                        if pos:
                            pos.update({"type": "position", "filename": name, "time": time.time()})
                            HUB.publish(pos)
                            print(f"[screenshots] position {pos['x']:.1f}, {pos['z']:.1f} from {name}")
                            if delete_after:
                                try:
                                    time.sleep(0.5)
                                    (d / name).unlink()
                                except OSError:
                                    pass
                    seen = names
            elif current_dir != folder:
                current_dir = folder
                print(f"[screenshots] folder not found: {folder!r}")
        except Exception as exc:
            print(f"[screenshots] error: {exc}")
        time.sleep(0.5)


_AUTO_LOGS_DIR = ""


def logs_dir() -> str:
    """The game's Logs folder: the one set in Settings, or the one found in the registry."""
    global _AUTO_LOGS_DIR
    with CONFIG_LOCK:
        custom = (CONFIG.get("logsDir") or "").strip()
    if custom:
        return custom
    if not _AUTO_LOGS_DIR:
        _AUTO_LOGS_DIR = game_logs.default_logs_dir()
    return _AUTO_LOGS_DIR


def log_watcher():
    """Follows the newest game session folder and publishes the game state when it changes."""
    follower = None
    state = game_logs.GameState()
    published = None
    while True:
        try:
            base = logs_dir()
            folder = game_logs.newest_log_folder(base) if base else None
            first = folder != (follower.folder if follower else None)
            if first:
                follower = game_logs.LogFollower(folder) if folder else None
                state = game_logs.GameState()
                print(f"[logs] reading {folder}" if folder else f"[logs] no game logs found in {base!r}")
            if follower:
                with CONFIG_LOCK:
                    auto_tick = bool(CONFIG.get("autoTick", True))
                    write_tt = bool(CONFIG.get("writeTT"))
                for entry in follower.read():
                    for ev in state.handle(*entry):
                        # logTime stops a message from being applied again after a restart
                        if ev["type"] != "task" or ev["time"] <= QUESTS.log_time():
                            continue
                        mode = ev.get("mode") or active_mode()
                        if write_tt and ev["status"] != "started" and token_for(mode):
                            QUESTS.queue_task(mode, ev["id"], "completed" if ev["status"] == "finished" else "failed")
                            HUB.publish({"type": "progress"})
                        if auto_tick:
                            QUESTS.apply_task_event(ev, active_mode())
                        else:
                            QUESTS.apply(mode, log_time=ev["time"])
                        print(f"[logs] task {ev['status']}: {ev['id']}")
                if use_game_mode(state.mode):
                    print(f"[logs] the game runs in {state.mode} mode: showing that mode")
                    HUB.publish({"type": "config"})
                state.expire(time.time())
            snap = state.snapshot()
            snap["session"] = os.path.basename(folder) if folder else None
            if snap != published:
                published = snap
                HUB.publish({"type": "game", **snap})
                r = snap["raid"]
                print(f"[logs] mode {snap['mode']}, raid {r['phase']} {r['location'] or r['scenePath'] or ''}".rstrip())
        except Exception as exc:
            print(f"[logs] error: {exc}")
        time.sleep(1)


# --------------------------------------------------------------------------- http

def tt_request(path: str, token: str, etag: str = None, body=None):
    """GET, or POST when a body is given. Returns (status, body bytes, headers)."""
    req = urllib.request.Request(TT_API + path, headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    if etag:
        req.add_header("If-None-Match", etag)
    if body is not None:
        req.data = json.dumps(body).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as err:
        return err.code, err.read(), dict(err.headers or {})


TOKEN_INFO = {}   # token -> list of permissions, or None when the check failed


def token_permissions(token: str):
    """GP = read, WP = write. Asked one time for each token."""
    if token and token not in TOKEN_INFO:
        try:
            status, body, _ = tt_request("/token", token)
            TOKEN_INFO[token] = list(json.loads(body).get("permissions") or []) if status == 200 else None
        except Exception:
            return None  # not reachable now: ask again later
    return TOKEN_INFO.get(token)


WRITE_DELAY = 3.0     # seconds without a new change before the changes are sent, so fast clicks make one write
WRITES = {"error": None, "retryAt": 0.0, "remaining": None, "backoff": 30.0}


def writes_status() -> dict:
    return {"type": "writes", "pending": QUESTS.pending_count(), "error": WRITES["error"],
            "remaining": WRITES["remaining"], "retryAt": WRITES["retryAt"]}


def _error_text(body: bytes) -> str:
    try:
        return str(json.loads(body).get("error") or "")[:200]
    except Exception:
        return body.decode("utf-8", "replace")[:200]


def send_writes(request=tt_request) -> bool:
    """Send the queued changes of each mode that has a token. True if all were sent.

    A refused change (400, 404: not in TarkovTracker's task list) is dropped. A 429
    or a network fault keeps the queue for a later try.
    """
    ok = True
    sent_any = False
    for mode, pending in QUESTS.pending().items():
        token = token_for(mode)
        if not token:
            continue
        calls = []
        tasks = pending["tasks"]
        if len(tasks) == 1:
            (task_id, state), = tasks.items()
            calls.append((f"/progress/task/{urllib.parse.quote(task_id, safe='')}", {"state": state}, [("tasks", task_id, state)]))
        elif tasks:
            calls.append(("/progress/tasks", [{"id": i, "state": st} for i, st in tasks.items()], [("tasks", i, st) for i, st in tasks.items()]))
        for objective_id, patch in pending["objectives"].items():
            calls.append((f"/progress/task/objective/{urllib.parse.quote(objective_id, safe='')}", patch, [("objectives", objective_id, patch)]))
        for path, body, items in calls:
            try:
                status, answer, headers = request(path, token, None, body)
            except Exception as exc:
                WRITES.update({"error": f"TarkovTracker not reachable: {exc}", "retryAt": time.time() + WRITES["backoff"]})
                WRITES["backoff"] = min(WRITES["backoff"] * 2, 600.0)
                return False
            low = {k.lower(): v for k, v in headers.items()}
            if "x-ratelimit-remaining" in low:
                WRITES["remaining"] = low["x-ratelimit-remaining"]
            if status == 200:
                sent_any = True
            elif status in (400, 404, 413):
                print(f"[tracker] change refused and dropped ({status}): {path}: {_error_text(answer)}")
                WRITES["error"] = f"TarkovTracker refused a change: {_error_text(answer) or status}"
            elif status == 429:
                try:
                    wait = float(low.get("retry-after") or 600)
                except ValueError:
                    wait = 600.0
                WRITES.update({"error": "TarkovTracker daily write limit reached. The changes are kept and sent later.",
                               "retryAt": time.time() + max(wait, 60.0)})
                return False
            else:
                msg = "the token is not valid or has no write permission" if status in (401, 403) else f"answer {status}"
                WRITES.update({"error": f"TarkovTracker: {msg}. The changes are kept.", "retryAt": time.time() + (600.0 if status in (401, 403) else WRITES["backoff"])})
                WRITES["backoff"] = min(WRITES["backoff"] * 2, 600.0)
                return False
            for kind, item_id, value in items:
                QUESTS.sent(mode, kind, item_id, value)
    if sent_any:
        WRITES.update({"backoff": 30.0, "retryAt": 0.0})
        if ok and not QUESTS.pending_count():
            WRITES["error"] = None if not (WRITES["error"] or "").startswith("TarkovTracker refused") else WRITES["error"]
        with PROGRESS_LOCK:
            PROGRESS_CACHE["time"] = 0.0   # the next read gets the new progress from TarkovTracker
    return ok


def write_worker():
    last = None
    while True:
        try:
            with CONFIG_LOCK:
                enabled = bool(CONFIG.get("writeTT"))
            now = time.time()
            if enabled and QUESTS.pending_count() and now - QUESTS.changed >= WRITE_DELAY and now >= WRITES["retryAt"]:
                send_writes()
                HUB.publish({"type": "progress"})
            status = writes_status()
            if status != last:
                last = status
                HUB.publish(status)
        except Exception as exc:
            print(f"[tracker] error: {exc}")
        time.sleep(0.5)


PROGRESS_CACHE = {"etag": None, "body": None, "token": None, "time": 0.0}
PROGRESS_LOCK = threading.Lock()


def _host_name(value: str) -> str:
    """Host name without the port: 'localhost:3000' -> 'localhost', '[::1]:3000' -> '[::1]'."""
    value = (value or "").strip().lower()
    if value.startswith("["):
        return value.split("]", 1)[0] + "]"
    return value.split(":", 1)[0]


def request_allowed(host: str, origin: str) -> bool:
    """Only the local page may talk to this server (stops CSRF and DNS rebinding)."""
    if _host_name(host) not in ALLOWED_HOSTS:
        return False
    if origin:
        m = re.match(r"^http://([^/]+)$", origin.strip().lower())
        if not m or _host_name(m.group(1)) not in ALLOWED_HOSTS:
            return False
    return True


class Handler(BaseHTTPRequestHandler):
    server_version = "RaidTaskMap/1.0"

    def log_message(self, fmt, *args):  # keep the console quiet
        pass

    def _send(self, status, body: bytes, ctype="application/json; charset=utf-8", extra=None):
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status, obj):
        self._send(status, json.dumps(obj).encode("utf-8"))

    def _public_config(self):
        cfg = self._config_fields()
        active = logs_dir()
        cfg["logsDirActive"] = active
        cfg["logsDirExists"] = bool(active) and os.path.isdir(active)
        return cfg

    def _config_fields(self):
        mode = active_mode()
        token = token_for(mode)
        hint = lambda t: (t[:4] + "…" + t[-4:]) if len(t) > 10 else "saved"
        with CONFIG_LOCK:
            fields = {
                "hasToken": bool(token),
                "tokenHint": hint(token) if token else "",
                "gameMode": mode,
                "tokens": {m: hint(t) for m, t in CONFIG["tokens"].items()},
                "screenshotsDir": CONFIG.get("screenshotsDir", ""),
                "screenshotsDirExists": os.path.isdir(CONFIG.get("screenshotsDir", "") or ""),
                "deleteScreenshots": bool(CONFIG.get("deleteScreenshots")),
                "logsDir": CONFIG.get("logsDir", ""),
                "autoTick": bool(CONFIG.get("autoTick", True)),
                "writeTT": bool(CONFIG.get("writeTT")),
            }
        # the permission check costs one request, so it is made only when writes are on
        perms = token_permissions(token) if fields["writeTT"] and token else None
        fields["canWrite"] = None if perms is None else "WP" in perms
        return fields

    def _allowed(self):
        if request_allowed(self.headers.get("Host", ""), self.headers.get("Origin", "")):
            return True
        self._json(403, {"error": "forbidden"})
        return False

    def do_GET(self):
        if not self._allowed():
            return
        path, _, query = self.path.partition("?")
        if path in ("/", "/index.html"):
            return self._static("index.html", "text/html; charset=utf-8")
        if path == "/maps.json":
            return self._static("maps.json", "application/json; charset=utf-8")
        if path == "/api/config":
            return self._json(200, self._public_config())
        if path == "/api/state":
            return self._json(200, HUB.state)
        if path == "/api/quests":
            return self._json(200, QUESTS.public())
        if path == "/api/writes":
            return self._json(200, writes_status())
        if path == "/api/progress":
            return self._progress(force="force=1" in query.split("&"))
        if path == "/api/events":
            return self._events()
        self._send(404, b'{"error":"not found"}')

    def do_POST(self):
        if not self._allowed():
            return
        # a JSON content type forces a CORS preflight, which this server never answers
        if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
            return self._json(415, {"error": "Content-Type must be application/json"})
        path = self.path.split("?", 1)[0]
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(data, dict):
                raise ValueError("not an object")
        except Exception:
            return self._json(400, {"error": "bad json"})
        if path == "/api/config":
            with CONFIG_LOCK:
                for key in ("screenshotsDir", "logsDir"):
                    if isinstance(data.get(key), str):
                        CONFIG[key] = data[key].strip()
                token = data.get("token").strip() if isinstance(data.get("token"), str) else ""
                if token:  # an empty field keeps the saved tokens; a token is saved for the mode of its prefix
                    CONFIG["tokens"][game_mode_for_token(token)] = token
                    CONFIG["mode"] = game_mode_for_token(token)
                if data.get("mode") in CONFIG["tokens"]:
                    CONFIG["mode"] = data["mode"]
                if data.get("removeToken") in CONFIG["tokens"]:
                    del CONFIG["tokens"][data["removeToken"]]
                for key in ("deleteScreenshots", "autoTick", "writeTT"):
                    if key in data:
                        CONFIG[key] = bool(data[key])
                if not CONFIG.get("screenshotsDir"):
                    CONFIG["screenshotsDir"] = default_screenshots_dir()
                save_config(CONFIG)
            with PROGRESS_LOCK:
                PROGRESS_CACHE.update({"etag": None, "body": None, "token": None, "time": 0.0})
            return self._json(200, self._public_config())
        if path == "/api/test-position":
            # lets you check the marker without starting the game
            try:
                ev = {"type": "position", "x": float(data.get("x", 0)), "y": float(data.get("y", 0)),
                      "z": float(data.get("z", 0)), "rotation": float(data.get("rotation", 0)),
                      "filename": "test", "time": time.time()}
            except (TypeError, ValueError):
                return self._json(400, {"error": "x, y, z and rotation must be numbers"})
            HUB.publish(ev)
            return self._json(200, ev)
        if path in ("/api/progress/task", "/api/progress/objective"):
            mode = active_mode()
            with CONFIG_LOCK:
                enabled = bool(CONFIG.get("writeTT"))
            if not enabled or not token_for(mode):
                return self._json(409, {"error": "Sending progress to TarkovTracker is off. Set it on in Settings."})
            item_id = data.get("id")
            if not isinstance(item_id, str) or not 0 < len(item_id.strip()) <= 64:
                return self._json(400, {"error": "id must be text of 1 to 64 characters"})
            if path.endswith("/task"):
                if data.get("state") not in ("completed", "uncompleted", "failed"):
                    return self._json(400, {"error": "state must be completed, uncompleted or failed"})
                QUESTS.queue_task(mode, item_id.strip(), data["state"])
            else:
                patch = {}
                if data.get("state") in ("completed", "uncompleted"):
                    patch["state"] = data["state"]
                count = data.get("count")
                if isinstance(count, (int, float)) and not isinstance(count, bool) and 0 <= count <= 100000:
                    patch["count"] = int(count)
                if not patch:
                    return self._json(400, {"error": "give a state (completed, uncompleted) or a count"})
                QUESTS.queue_objective(mode, item_id.strip(), patch)
            HUB.publish({"type": "progress"})
            return self._json(200, writes_status())
        if path == "/api/quests":
            mode = data.get("mode")
            lists = [data.get(k, []) for k in ("add", "remove", "addCustom", "removeCustom")]
            if mode not in GAME_MODES or not all(isinstance(x, list) and all(isinstance(i, str) and 0 < len(i) <= 200 for i in x) for x in lists):
                return self._json(400, {"error": "mode must be a game mode; add, remove, addCustom and removeCustom must be lists of text"})
            return self._json(200, QUESTS.apply(mode, *lists, migrated=bool(data.get("migrated"))))
        if path == "/api/past-logs":
            # with "apply": false this only reports what the old logs say
            token_mode = active_mode()
            events = game_logs.task_events(logs_dir()) if logs_dir() else []
            for ev in events:
                ev["mode"] = ev["mode"] or token_mode
            changes = game_logs.net_task_changes(events)
            if data.get("apply"):
                latest = max((ev["time"] for ev in events), default=None)
                for mode, c in changes.items():
                    QUESTS.apply(mode, add=c["started"], remove=c["ended"], log_time=latest)
            return self._json(200, {"changes": changes, "messages": len(events), "applied": bool(data.get("apply"))})
        if path == "/api/test-task":
            # lets you check the automatic ticks without the game
            if data.get("status") not in ("started", "finished", "failed") or not isinstance(data.get("id"), str):
                return self._json(400, {"error": "status must be started, finished or failed; id must be text"})
            token_mode = active_mode()
            ev = {"type": "task", "status": data["status"], "id": data["id"], "time": time.time(), "mode": data.get("mode")}
            return self._json(200, QUESTS.apply_task_event(ev, token_mode))
        if path == "/api/test-game":
            # lets you check the raid behaviour without starting the game; the next log change replaces it
            raid = game_logs.new_raid()
            raid.update({k: data[k] for k in raid if k in data})
            ev = {"type": "game", "mode": data.get("mode"), "raid": raid, "session": "test"}
            HUB.publish(ev)
            return self._json(200, ev)
        self._send(404, b'{"error":"not found"}')

    def _static(self, name, ctype):
        p = APP_DIR / name
        if not p.exists():
            return self._send(404, b"missing file")
        self._send(200, p.read_bytes(), ctype)

    def _progress(self, force=False):
        mode = active_mode()
        token = token_for(mode)
        if not token:
            return self._json(400, {"error": "No TarkovTracker token set. Open Settings and paste your token."})

        def send(body, stale=False):
            self._send(200, overlay_progress(body, QUESTS.pending(mode)), extra={"X-Stale": "1"} if stale else None)

        # one lock for the whole call: several tabs then share one upstream read
        with PROGRESS_LOCK:
            cached = PROGRESS_CACHE["body"] if PROGRESS_CACHE["token"] == token else None
            age = time.time() - PROGRESS_CACHE["time"]
            if cached and age < (PROGRESS_FORCE_AGE if force else PROGRESS_MIN_AGE):
                return send(cached)
            try:
                status, body, headers = tt_request("/progress", token, PROGRESS_CACHE["etag"] if cached else None)
                if status == 304 and not cached:
                    status, body, headers = tt_request("/progress", token)
            except Exception as exc:
                if cached:
                    return send(cached, stale=True)
                return self._json(502, {"error": f"Could not reach TarkovTracker: {exc}"})
            if status == 304:
                PROGRESS_CACHE["time"] = time.time()
                return send(cached)
            if status == 200:
                PROGRESS_CACHE.update({"etag": headers.get("ETag") or headers.get("etag"),
                                       "body": body, "token": token, "time": time.time()})
                return send(body)
            if cached and (status == 429 or status >= 500):
                return send(cached, stale=True)
        try:
            msg = json.loads(body).get("error") or body.decode("utf-8", "replace")
        except Exception:
            msg = body.decode("utf-8", "replace")[:300]
        return self._json(status, {"error": f"TarkovTracker answered {status}: {msg}"})

    def _events(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        q = HUB.subscribe()
        try:
            while True:
                try:
                    ev = q.get(timeout=15)
                    self.wfile.write(f"data: {json.dumps(ev)}\n\n".encode("utf-8"))
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
            pass
        finally:
            HUB.unsubscribe(q)


class Server(ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # a browser that closes a connection early (page reload, closed tab) is not a fault
        if isinstance(sys.exc_info()[1], (ConnectionError, TimeoutError)):
            return
        super().handle_error(request, client_address)


def main():
    threading.Thread(target=screenshot_watcher, daemon=True).start()
    threading.Thread(target=log_watcher, daemon=True).start()
    threading.Thread(target=write_worker, daemon=True).start()
    try:
        server = Server(("127.0.0.1", PORT), Handler)
    except OSError as exc:
        print(f"Could not start on port {PORT}: {exc}\nIs it already running? Use --port to select another port, for example: --port 3005")
        input("Press Enter to close.")
        sys.exit(1)
    server.daemon_threads = True
    url = f"http://localhost:{PORT}/"
    print(f"{APP_NAME} running at {url}  (press Ctrl+C to stop)")
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
