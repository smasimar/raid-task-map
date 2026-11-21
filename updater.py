"""Looks for a newer version of the app on GitHub and installs it.

Two kinds of install:
  git    the folder is a git clone: "git fetch" from GitHub, then a fast-forward merge.
         A folder with local commits that GitHub does not have is never changed.
  files  the folder came from a ZIP download: the files are compared with the newest commit
         on GitHub by their git blob hashes, and the changed files are taken from the ZIP of
         that commit. config.json and state.json are not in the repository, so they stay.

After an update the app must start again to use the new files.
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
import threading
import time
import urllib.request
import zipfile
from pathlib import Path

REPO = "smasimar/raid-task-map"
BRANCH = "main"
API = f"https://api.github.com/repos/{REPO}"
GIT_URL = f"https://github.com/{REPO}.git"
ZIP_URL = f"https://codeload.github.com/{REPO}/zip/{{sha}}"
USER_AGENT = "RaidTaskMap-updater"
RECORD = ".installed-commit"   # files install: the commit that the files came from


def http_get(url: str, timeout: float = 20) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def blob_sha(data: bytes) -> str:
    """The hash that git gives a file's content."""
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def same_file(path: Path, sha: str) -> bool:
    """True if the file has the content of the git blob. A text file with Windows line ends also counts."""
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return blob_sha(data) == sha or (b"\r\n" in data and blob_sha(data.replace(b"\r\n", b"\n")) == sha)


class Updater:
    def __init__(self, app_dir: Path, publish=lambda ev: None, get=http_get, git=None, git_url=GIT_URL):
        self.dir = Path(app_dir)
        self.git_url = git_url
        self.publish = publish
        self.get = get
        self.git_cmd = git if git is not None else shutil.which("git")
        self.lock = threading.Lock()
        self.status = {"state": "idle", "method": self.method(), "local": self.local_version(),
                       "remote": None, "message": "", "behind": None, "changed": [], "error": "",
                       "checked": None, "startedAt": time.time()}

    # ---------------------------------------------------------------- what is installed
    def method(self) -> str:
        return "git" if self.git_cmd and (self.dir / ".git").exists() else "files"

    def _git(self, *args, timeout=60) -> str:
        r = subprocess.run([self.git_cmd, *args], cwd=self.dir, capture_output=True, text=True, timeout=timeout,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip().splitlines()[-1] if (r.stderr or r.stdout).strip() else f"git {args[0]} failed")
        return r.stdout.strip()

    def local_version(self):
        try:
            if self.method() == "git":
                return self._git("rev-parse", "HEAD")
            return (self.dir / RECORD).read_text(encoding="utf-8").strip() or None
        except Exception:
            return None

    # ---------------------------------------------------------------- state
    def _set(self, **changes):
        with self.lock:
            self.status.update(changes)
            snap = dict(self.status)
        self.publish({"type": "update", **snap})
        return snap

    def snapshot(self):
        with self.lock:
            return dict(self.status)

    def busy(self) -> bool:
        return self.snapshot()["state"] in ("checking", "updating")

    # ---------------------------------------------------------------- check
    def check(self):
        """Look for a newer commit. The state becomes "current", "available" or "error"."""
        self._set(state="checking", error="")
        try:
            if self.method() == "git":
                return self._check_git()
            return self._check_files()
        except Exception as exc:
            return self._set(state="error", error=f"Could not check for updates: {exc}", checked=time.time())

    def _check_git(self):
        self._git("fetch", "--quiet", self.git_url, BRANCH)
        remote = self._git("rev-parse", "FETCH_HEAD")
        local = self._git("rev-parse", "HEAD")
        behind = int(self._git("rev-list", "--count", "HEAD..FETCH_HEAD"))
        message = self._git("log", "-1", "--format=%s", "FETCH_HEAD")
        return self._set(state="available" if behind else "current", local=local, remote=remote,
                         behind=behind, message=message, changed=[], checked=time.time())

    def _check_files(self):
        head = json.loads(self.get(f"{API}/commits/{BRANCH}"))
        remote = head["sha"]
        message = (head.get("commit", {}).get("message") or "").splitlines()[0]
        tree = json.loads(self.get(f"{API}/git/trees/{remote}?recursive=1"))
        changed = [e["path"] for e in tree.get("tree", [])
                   if e.get("type") == "blob" and not same_file(self.dir / e["path"], e["sha"])]
        if not changed and self.status.get("local") != remote:
            self._record(remote)
        return self._set(state="available" if changed else "current", local=self.local_version(), remote=remote,
                         behind=None, message=message, changed=changed, checked=time.time())

    def _record(self, sha: str):
        try:
            (self.dir / RECORD).write_text(sha + "\n", encoding="utf-8")
        except OSError:
            pass

    # ---------------------------------------------------------------- update
    def update(self):
        """Install the newest version. The state becomes "updated" (start the app again) or "error"."""
        snap = self.snapshot()
        if snap["state"] != "available":
            return snap
        self._set(state="updating", error="")
        try:
            if self.method() == "git":
                self._git("fetch", "--quiet", self.git_url, BRANCH)
                self._git("merge", "--ff-only", "--quiet", "FETCH_HEAD")
            else:
                self._update_files(snap["remote"], snap["changed"])
            return self._set(state="updated", local=self.local_version(), behind=0, changed=[])
        except Exception as exc:
            hint = " The folder has local changes; update it with git yourself." if self.method() == "git" else ""
            return self._set(state="error", error=f"The update failed: {exc}.{hint}")

    def _update_files(self, sha: str, changed: list):
        data = self.get(ZIP_URL.format(sha=sha), timeout=60)
        root = self.dir.resolve()
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            prefix = z.namelist()[0].split("/")[0] + "/"   # "raid-task-map-<sha>/"
            wanted = set(changed)
            for info in z.infolist():
                rel = info.filename[len(prefix):] if info.filename.startswith(prefix) else ""
                if not rel or info.is_dir() or rel not in wanted:
                    continue
                target = (root / rel).resolve()
                if root not in target.parents:          # a path that leaves the app folder
                    continue
                target.parent.mkdir(parents=True, exist_ok=True)
                tmp = target.with_name(target.name + ".update-tmp")
                tmp.write_bytes(z.read(info))
                os.replace(tmp, target)
        self._record(sha)
