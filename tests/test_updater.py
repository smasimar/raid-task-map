"""Update tests. Run from the project folder:  py -3 -m unittest discover tests

GitHub is not contacted: the files install gets a fake HTTP function, and the git install
fetches from a local repository that stands in for GitHub.
"""
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import updater  # noqa: E402

NEW_SHA = "b" * 40


def fake_github(files: dict):
    """An HTTP function that answers like GitHub for one commit that holds `files`."""
    tree = {"tree": [{"path": p, "type": "blob", "sha": updater.blob_sha(c)} for p, c in files.items()]}
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr(f"raid-task-map-{NEW_SHA}/", "")
        for p, c in files.items():
            z.writestr(f"raid-task-map-{NEW_SHA}/{p}", c)
        z.writestr(f"raid-task-map-{NEW_SHA}/../evil.txt", b"x")   # must not leave the folder
    answers = {
        f"{updater.API}/commits/{updater.BRANCH}": json.dumps({"sha": NEW_SHA, "commit": {"message": "Add things\n\nmore"}}).encode(),
        f"{updater.API}/git/trees/{NEW_SHA}?recursive=1": json.dumps(tree).encode(),
        updater.ZIP_URL.format(sha=NEW_SHA): buf.getvalue(),
    }
    calls = []

    def get(url, timeout=20):
        calls.append(url)
        return answers[url]
    get.calls = calls
    return get


class Files(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name) / "app"
        self.dir.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_blob_sha_is_the_git_hash(self):
        self.assertEqual(updater.blob_sha(b"hello\n"), "ce013625030ba8dba906f756967f9e9ca394464a")

    def test_windows_line_ends_count_as_the_same_file(self):
        (self.dir / "a.txt").write_bytes(b"one\r\ntwo\r\n")
        self.assertTrue(updater.same_file(self.dir / "a.txt", updater.blob_sha(b"one\ntwo\n")))
        self.assertFalse(updater.same_file(self.dir / "a.txt", updater.blob_sha(b"one\nthree\n")))
        self.assertFalse(updater.same_file(self.dir / "missing.txt", updater.blob_sha(b"")))

    def test_check_finds_the_changed_files_and_update_installs_them(self):
        (self.dir / "same.py").write_bytes(b"print(1)\r\n")
        (self.dir / "old.py").write_bytes(b"print('old')\n")
        (self.dir / "config.json").write_text('{"tokens": {"pve": "secret"}}')
        files = {"same.py": b"print(1)\n", "old.py": b"print('new')\n", "docs/new.md": b"# new\n"}
        events = []
        up = updater.Updater(self.dir, events.append, get=fake_github(files), git="")
        self.assertEqual(up.method(), "files")
        st = up.check()
        self.assertEqual((st["state"], st["remote"], st["message"]), ("available", NEW_SHA, "Add things"))
        self.assertEqual(sorted(st["changed"]), ["docs/new.md", "old.py"])
        st = up.update()
        self.assertEqual(st["state"], "updated")
        self.assertEqual((self.dir / "old.py").read_bytes(), b"print('new')\n")
        self.assertEqual((self.dir / "docs/new.md").read_bytes(), b"# new\n")
        self.assertEqual((self.dir / "same.py").read_bytes(), b"print(1)\r\n", "an unchanged file is not written")
        self.assertIn("secret", (self.dir / "config.json").read_text(), "the settings stay")
        self.assertFalse((self.dir.parent / "evil.txt").exists(), "nothing is written outside the app folder")
        self.assertEqual(up.local_version(), NEW_SHA)
        self.assertEqual([e["state"] for e in events], ["checking", "available", "updating", "updated"])
        # the next check finds nothing new
        self.assertEqual(updater.Updater(self.dir, get=fake_github(files), git="").check()["state"], "current")

    def test_patch_notes_mark_the_new_changes(self):
        commits = [
            {"sha": "c" * 40, "commit": {"message": "Newest\n\n- detail\n\nCo-Authored-By: X <x@example.com>", "committer": {"date": "2026-11-22T10:00:00Z"}}},
            {"sha": "a" * 40, "commit": {"message": "Installed", "committer": {"date": "2026-11-21T10:00:00Z"}}},
            {"sha": "9" * 40, "commit": {"message": "Older", "committer": {"date": "2026-11-20T10:00:00Z"}}},
        ]
        (self.dir / updater.RECORD).write_text("a" * 40)
        up = updater.Updater(self.dir, get=lambda url, timeout=20: json.dumps(commits).encode(), git="")
        notes = up.notes()
        self.assertEqual([n["subject"] for n in notes], ["Newest", "Installed", "Older"])
        self.assertEqual([n["installed"] for n in notes], [False, True, True])
        self.assertEqual(notes[0]["body"], "- detail", "the co-author line is left out")
        (self.dir / updater.RECORD).unlink()
        self.assertEqual({n["installed"] for n in up.notes()}, {None}, "unknown when the installed version is not known")

    def test_update_does_nothing_without_a_found_version(self):
        get = fake_github({"a.py": b"x"})
        up = updater.Updater(self.dir, get=get, git="")
        self.assertEqual(up.update()["state"], "idle")
        self.assertEqual(get.calls, [])

    def test_a_network_fault_is_an_error_state(self):
        def get(url, timeout=20):
            raise OSError("no network")
        st = updater.Updater(self.dir, get=get, git="").check()
        self.assertEqual(st["state"], "error")
        self.assertIn("no network", st["error"])


@unittest.skipUnless(shutil.which("git"), "git is not installed")
class Git(unittest.TestCase):
    def git(self, cwd, *args):
        return subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@example.com", *args], cwd=cwd,
                              capture_output=True, text=True, check=True).stdout.strip()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.hub, self.app = base / "hub", base / "app"
        self.hub.mkdir()
        self.git(self.hub, "init", "-q", "-b", updater.BRANCH)
        (self.hub / "a.py").write_text("v1\n")
        self.git(self.hub, "add", "-A")
        self.git(self.hub, "commit", "-q", "-m", "First")
        self.git(base, "clone", "-q", str(self.hub), str(self.app))

    def tearDown(self):
        self.tmp.cleanup()

    def updater(self):
        return updater.Updater(self.app, git_url=str(self.hub))

    def test_current_then_a_new_commit_is_found_and_merged(self):
        self.assertEqual(self.updater().check()["state"], "current")
        (self.hub / "a.py").write_text("v2\n")
        self.git(self.hub, "commit", "-q", "-am", "Second")
        up = self.updater()
        st = up.check()
        self.assertEqual((st["state"], st["behind"], st["message"]), ("available", 1, "Second"))
        self.assertEqual(up.update()["state"], "updated")
        self.assertEqual((self.app / "a.py").read_text(), "v2\n")
        self.assertEqual(up.local_version(), self.git(self.hub, "rev-parse", "HEAD"))

    def test_local_commits_are_never_changed(self):
        (self.app / "b.py").write_text("mine\n")
        self.git(self.app, "add", "-A")
        self.git(self.app, "commit", "-q", "-m", "Mine")
        self.assertEqual(self.updater().check()["state"], "current", "a clone ahead of GitHub has nothing to update")
        (self.hub / "a.py").write_text("v2\n")
        self.git(self.hub, "commit", "-q", "-am", "Second")
        up = self.updater()
        self.assertEqual(up.check()["state"], "available")
        st = up.update()
        self.assertEqual(st["state"], "error", "branches that went apart need the user")
        self.assertEqual((self.app / "a.py").read_text(), "v1\n")


if __name__ == "__main__":
    unittest.main()
