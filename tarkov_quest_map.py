#!/usr/bin/env python3
"""
Tarkov Quest Map - a small local replacement for the Tarkov.dev map.

What it does
  * Serves a map page at http://localhost:3000
  * Reads your progress from TarkovTracker.org (api.tarkovtracker.org) with your API token
  * Watches the EFT screenshots folder: every new screenshot moves your marker on the map
  * Never writes to TarkovTracker: TarkovMonitor keeps your progress up to date

Only the Python standard library is used. Run:  python tarkov_quest_map.py
"""
import json
import os
import queue
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import game_logs

APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "config.json"
PORT = int(os.environ.get("TQM_PORT", "3000"))
if "--port" in sys.argv[1:-1]:
    PORT = int(sys.argv[sys.argv.index("--port") + 1])
TT_API = "https://api.tarkovtracker.org"
USER_AGENT = "TarkovQuestMap/1.0 (local)"

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
    cfg = {"token": "", "screenshotsDir": "", "deleteScreenshots": False, "logsDir": ""}
    if CONFIG_PATH.exists():
        try:
            cfg.update(json.loads(CONFIG_PATH.read_text(encoding="utf-8")))
        except Exception as exc:
            print(f"[config] could not read config.json: {exc}")
    if not cfg.get("screenshotsDir"):
        cfg["screenshotsDir"] = default_screenshots_dir()
    return cfg


def save_config(cfg: dict) -> None:
    tmp = CONFIG_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    os.replace(tmp, CONFIG_PATH)


CONFIG = load_config()
CONFIG_LOCK = threading.Lock()


def game_mode_for_token(token: str) -> str:
    """json.tarkov.dev game mode that matches the TarkovTracker token prefix."""
    t = (token or "").upper()
    if t.startswith("PVE_"):
        return "pve"
    if t.startswith("SZN_"):
        return "pvp-season"
    return "regular"


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
                for entry in follower.read():
                    for ev in state.handle(*entry):
                        # entries that were in the log before this app started are history
                        if ev["type"] == "task" and not first:
                            print(f"[logs] task {ev['status']}: {ev['id']}")
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

def tt_request(path: str, token: str, etag: str = None):
    req = urllib.request.Request(TT_API + path, headers={
        "Authorization": f"Bearer {token}",
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    if etag:
        req.add_header("If-None-Match", etag)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read(), dict(resp.headers)
    except urllib.error.HTTPError as err:
        return err.code, err.read(), dict(err.headers or {})


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
    server_version = "TarkovQuestMap/1.0"

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
        with CONFIG_LOCK:
            token = CONFIG.get("token") or ""
            return {
                "hasToken": bool(token),
                "tokenHint": (token[:4] + "…" + token[-4:]) if len(token) > 10 else "",
                "gameMode": game_mode_for_token(token),
                "screenshotsDir": CONFIG.get("screenshotsDir", ""),
                "screenshotsDirExists": os.path.isdir(CONFIG.get("screenshotsDir", "") or ""),
                "deleteScreenshots": bool(CONFIG.get("deleteScreenshots")),
                "logsDir": CONFIG.get("logsDir", ""),
            }

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
                for key in ("token", "screenshotsDir", "logsDir"):
                    if key in data and isinstance(data[key], str):
                        val = data[key].strip()
                        if key == "token" and not val:
                            continue  # empty token field = keep current
                        CONFIG[key] = val
                if "deleteScreenshots" in data:
                    CONFIG["deleteScreenshots"] = bool(data["deleteScreenshots"])
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
        with CONFIG_LOCK:
            token = CONFIG.get("token") or ""
        if not token:
            return self._json(400, {"error": "No TarkovTracker token set. Open Settings and paste your token."})
        # one lock for the whole call: several tabs then share one upstream read
        with PROGRESS_LOCK:
            cached = PROGRESS_CACHE["body"] if PROGRESS_CACHE["token"] == token else None
            age = time.time() - PROGRESS_CACHE["time"]
            if cached and age < (PROGRESS_FORCE_AGE if force else PROGRESS_MIN_AGE):
                return self._send(200, cached)
            try:
                status, body, headers = tt_request("/progress", token, PROGRESS_CACHE["etag"] if cached else None)
                if status == 304 and not cached:
                    status, body, headers = tt_request("/progress", token)
            except Exception as exc:
                if cached:
                    return self._send(200, cached, extra={"X-Stale": "1"})
                return self._json(502, {"error": f"Could not reach TarkovTracker: {exc}"})
            if status == 304:
                PROGRESS_CACHE["time"] = time.time()
                return self._send(200, cached)
            if status == 200:
                PROGRESS_CACHE.update({"etag": headers.get("ETag") or headers.get("etag"),
                                       "body": body, "token": token, "time": time.time()})
                return self._send(200, body)
            if cached and (status == 429 or status >= 500):
                return self._send(200, cached, extra={"X-Stale": "1"})
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


def main():
    threading.Thread(target=screenshot_watcher, daemon=True).start()
    threading.Thread(target=log_watcher, daemon=True).start()
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError as exc:
        print(f"Could not start on port {PORT}: {exc}\nIs it already running? Set TQM_PORT to use another port.")
        input("Press Enter to close.")
        sys.exit(1)
    server.daemon_threads = True
    url = f"http://localhost:{PORT}/"
    print(f"Tarkov Quest Map running at {url}  (close this window to stop)")
    if "--no-browser" not in sys.argv:
        threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
