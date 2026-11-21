"""Server unit tests. Run from the project folder:  py -3 -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import raid_task_map as app  # noqa: E402


class ParseScreenshot(unittest.TestCase):
    def test_normal_name(self):
        pos = app.parse_screenshot("2024-08-13[22-41]_351.48, 1.07, 73.79_0.0, -0.9, 0.0, 0.4_13.27 (0).png")
        self.assertEqual((pos["x"], pos["y"], pos["z"]), (351.48, 1.07, 73.79))
        self.assertAlmostEqual(pos["rotation"], -130.73, places=1)

    def test_screenshot_number_above_9(self):
        pos = app.parse_screenshot("2024-08-13[22-41]_-351.48, -1.07, 73.79_0.00000, -0.98765, 0.0, 0.4_13.27 (12).png")
        self.assertEqual(pos["x"], -351.48)

    def test_exponent_quaternion(self):
        self.assertIsNotNone(
            app.parse_screenshot("2024-08-13[22-41]_351.48, 1.07, 73.79_1E-05, -0.9, 0.0, 0.4_13.27 (1).png"))

    def test_other_files(self):
        self.assertIsNone(app.parse_screenshot("holiday.png"))
        self.assertIsNone(app.parse_screenshot("2024-08-13[22-41]_no position (0).png"))


class RequestAllowed(unittest.TestCase):
    def test_local(self):
        self.assertTrue(app.request_allowed("localhost:3000", ""))
        self.assertTrue(app.request_allowed("127.0.0.1:3000", "http://localhost:3000"))
        self.assertTrue(app.request_allowed("[::1]:3000", "http://[::1]:3000"))

    def test_foreign(self):
        self.assertFalse(app.request_allowed("evil.example:3000", ""))          # DNS rebinding
        self.assertFalse(app.request_allowed("localhost:3000", "https://evil.example"))  # cross-site POST
        self.assertFalse(app.request_allowed("localhost:3000", "null"))
        self.assertFalse(app.request_allowed("", ""))


class GameMode(unittest.TestCase):
    def test_prefix(self):
        self.assertEqual(app.game_mode_for_token("PVE_abc"), "pve")
        self.assertEqual(app.game_mode_for_token("SZN_abc"), "pvp-season")
        self.assertEqual(app.game_mode_for_token("PVP_abc"), "regular")


class Quests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "state.json"
        self.events = []
        self.q = app.QuestList(self.path, self.events.append)

    def tearDown(self):
        self.dir.cleanup()

    def test_add_remove_and_reload(self):
        self.q.apply("pve", add=["a", "b", "a"], add_custom=["New Quest"])
        self.q.apply("pve", remove=["a"], add_custom=["new quest"])
        self.q.apply("regular", add=["z"])
        again = app.QuestList(self.path).public()
        self.assertEqual(again["modes"], {"pve": {"selected": ["b"], "custom": ["New Quest"]}, "regular": {"selected": ["z"], "custom": []}})
        self.assertEqual([e["mode"] for e in self.events], ["pve", "pve", "regular"])

    def test_no_event_without_a_change(self):
        self.q.apply("pve", add=["a"])
        self.q.apply("pve", add=["a"])
        self.assertEqual(len(self.events), 1)

    def test_task_messages(self):
        task = lambda status, when, mode="pve": {"type": "task", "status": status, "id": "a", "time": when, "mode": mode}
        self.q.apply_task_event(task("started", 100.0), "regular")
        self.assertEqual(self.q.public()["modes"]["pve"]["selected"], ["a"])
        self.assertEqual(self.events[-1]["note"], {"status": "started", "id": "a"})
        self.q.apply_task_event(task("finished", 200.0), "regular")
        self.assertEqual(self.q.public()["modes"]["pve"]["selected"], [])
        self.assertEqual(self.q.log_time(), 200.0)
        # a log without a mode line uses the mode of the token
        self.q.apply_task_event(task("started", 300.0, None), "regular")
        self.assertEqual(self.q.public()["modes"]["regular"]["selected"], ["a"])
        self.assertEqual(app.QuestList(self.path).log_time(), 300.0)

    def test_migrated_flag(self):
        self.q.apply("pve", add=["a"], migrated=True)
        self.assertEqual(self.q.public()["migrated"], ["pve"])


class Status(unittest.TestCase):
    def test_note_goes_to_the_activity_list(self):
        before = len(app.ACTIVITY)
        app.note("task", "finished in the game", taskId="abc", status="finished")
        item = app.ACTIVITY[-1]
        self.assertEqual((item["kind"], item["text"], item["err"], item["taskId"]), ("task", "finished in the game", False, "abc"))
        self.assertEqual(len(app.ACTIVITY), min(before + 1, app.ACTIVITY.maxlen))

    def test_raid_text(self):
        raid = dict(app.game_logs.new_raid(), scenePath="maps/woods_preset.bundle")
        self.assertEqual(app.raid_text(dict(raid, phase="loading"), "idle"), "loading woods")
        self.assertEqual(app.raid_text(dict(raid, phase="raid", side="scav"), "starting"), "raid started on woods · Scav · local")
        self.assertEqual(app.raid_text(dict(raid, phase="raid", side="pmc", online=True, location="Woods"), "starting"), "raid started on Woods · PMC · online")
        self.assertEqual(app.raid_text(dict(raid, phase="idle"), "raid"), "raid ended")
        self.assertEqual(app.raid_text(dict(raid, phase="idle"), "idle"), "not in a raid")

    def test_status_report_has_no_token_text(self):
        import json
        report = app.status_report()
        for key in ("logLines", "logsFound", "shotsFound", "trackerOk", "writes", "activity", "mode", "hasToken", "canWrite"):
            self.assertIn(key, report)
        for token in app.CONFIG["tokens"].values():
            self.assertNotIn(token, json.dumps(report))


class Tokens(unittest.TestCase):
    def test_old_single_token_moves_to_its_mode(self):
        import json, tempfile
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "config.json"
            path.write_text(json.dumps({"token": "PVE_abcdefghijkl"}), encoding="utf-8")
            real, app.CONFIG_PATH = app.CONFIG_PATH, path
            try:
                cfg = app.load_config()
            finally:
                app.CONFIG_PATH = real
        self.assertEqual(cfg["tokens"], {"pve": "PVE_abcdefghijkl"})
        self.assertNotIn("token", cfg)
        self.assertFalse(cfg["writeTT"])
        self.assertTrue(cfg["autoUpdate"], "the update check is on by default")


class UpdateRoutes(unittest.TestCase):
    """The page talks to the updater through /api/update; GitHub is not contacted here."""

    def setUp(self):
        import threading
        self.server = app.Server(("127.0.0.1", 0), app.Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.base = f"http://127.0.0.1:{self.server.server_address[1]}"
        self.real = app.UPDATER

    def tearDown(self):
        app.UPDATER = self.real
        app.RESTART.clear()
        self.server.shutdown()
        self.server.server_close()

    def call(self, path, body=None):
        import json, urllib.request, urllib.error
        req = urllib.request.Request(self.base + path, data=None if body is None else json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            return e.code, json.loads(e.read())

    def test_status_check_and_restart(self):
        import updater, threading
        done = threading.Event()

        class Fake(updater.Updater):
            def check(self):
                st = self._set(state="current", local="a" * 40)
                done.set()
                return st
        app.UPDATER = Fake(Path("."), git="")
        status, st = self.call("/api/update")
        self.assertEqual((status, st["state"]), (200, "idle"))
        status, _ = self.call("/api/update/check", {})
        self.assertEqual(status, 202)
        self.assertTrue(done.wait(5))
        self.assertEqual(self.call("/api/update")[1]["state"], "current")
        status, body = self.call("/api/update/restart", {})
        self.assertEqual(status, 409, "no restart without an installed update")
        self.assertFalse(app.RESTART.is_set())


class Overlay(unittest.TestCase):
    BODY = b'{"data": {"tasksProgress": [{"id": "a", "complete": false}], "taskObjectivesProgress": [{"id": "o1", "complete": false, "count": 2}]}}'

    def test_nothing_pending_keeps_the_bytes(self):
        self.assertIs(app.overlay_progress(self.BODY, {"tasks": {}, "objectives": {}}), self.BODY)

    def test_pending_changes_show(self):
        import json
        out = json.loads(app.overlay_progress(self.BODY, {"tasks": {"a": "completed", "b": "failed"},
                                                         "objectives": {"o1": {"count": 5}, "o2": {"state": "completed"}}}))["data"]
        self.assertEqual(out["tasksProgress"], [{"id": "a", "complete": True, "failed": False}, {"id": "b", "complete": False, "failed": True}])
        self.assertEqual(out["taskObjectivesProgress"], [{"id": "o1", "complete": False, "count": 5}, {"id": "o2", "complete": True}])

    def test_pending_level_shows(self):
        import json
        out = json.loads(app.overlay_progress(self.BODY, {"tasks": {}, "objectives": {}, "level": {"player": 21}}))["data"]
        self.assertEqual(out["playerLevel"], 21)


class Writes(unittest.TestCase):
    """send_writes with a stand-in for TarkovTracker."""

    def setUp(self):
        import tempfile
        self.dir = tempfile.TemporaryDirectory()
        self.saved = (app.QUESTS, dict(app.CONFIG), dict(app.WRITES))
        app.QUESTS = app.QuestList(Path(self.dir.name) / "state.json")
        app.CONFIG.clear()
        app.CONFIG.update({"tokens": {"pve": "PVE_testtoken0001"}, "mode": "pve", "writeTT": True})
        self.calls = []
        self.answer = (200, b'{"success": true}', {"X-RateLimit-Remaining": "97"})

    def tearDown(self):
        app.QUESTS = self.saved[0]
        app.CONFIG.clear(); app.CONFIG.update(self.saved[1])
        app.WRITES.clear(); app.WRITES.update(self.saved[2])
        self.dir.cleanup()

    def request(self, path, token, etag, body):
        self.calls.append((path, body))
        if isinstance(self.answer, Exception):
            raise self.answer
        return self.answer

    def test_fast_clicks_on_one_step_make_one_write(self):
        for n in range(1, 11):
            app.QUESTS.queue_objective("pve", "o1", {"count": n, "state": "uncompleted"})
        self.assertTrue(app.send_writes(self.request))
        self.assertEqual(self.calls, [("/progress/task/objective/o1", {"count": 10, "state": "uncompleted"})])
        self.assertEqual(app.QUESTS.pending_count(), 0)
        self.assertEqual(app.WRITES["remaining"], "97")

    def test_level_sends_the_last_value(self):
        app.QUESTS.queue_level("pve", 14)
        app.QUESTS.queue_level("pve", 15)
        self.assertEqual(app.QUESTS.pending_count(), 1)
        self.assertTrue(app.send_writes(self.request))
        self.assertEqual(self.calls, [("/progress/level/15", {})])
        self.assertEqual(app.QUESTS.pending_count(), 0)

    def test_state_file_without_level(self):
        import json
        app.QUESTS.path.write_text(json.dumps({"writes": {"pve": {"tasks": {"a": "completed"}, "objectives": {}}}}), encoding="utf-8")
        old = app.QuestList(app.QUESTS.path)
        self.assertEqual(old.pending_count(), 1)
        self.assertEqual(old.pending("pve")["level"], {})

    def test_one_task_and_many_tasks(self):
        app.QUESTS.queue_task("pve", "a", "completed")
        app.send_writes(self.request)
        app.QUESTS.queue_task("pve", "a", "uncompleted")
        app.QUESTS.queue_task("pve", "b", "failed")
        app.send_writes(self.request)
        self.assertEqual(self.calls, [("/progress/task/a", {"state": "completed"}),
                                      ("/progress/tasks", [{"id": "a", "state": "uncompleted"}, {"id": "b", "state": "failed"}])])

    def test_limit_reached_keeps_the_queue(self):
        app.QUESTS.queue_task("pve", "a", "completed")
        self.answer = (429, b'{"success": false, "error": "quota"}', {"Retry-After": "120"})
        self.assertFalse(app.send_writes(self.request))
        self.assertEqual(app.QUESTS.pending("pve")["tasks"], {"a": "completed"})
        self.assertGreater(app.WRITES["retryAt"], app.time.time() + 100)
        self.assertIn("limit", app.WRITES["error"])
        # the queue is on disk, so it is still there after a restart
        self.assertEqual(app.QuestList(app.QUESTS.path).pending("pve")["tasks"], {"a": "completed"})

    def test_network_fault_keeps_the_queue(self):
        app.QUESTS.queue_task("pve", "a", "completed")
        self.answer = OSError("offline")
        self.assertFalse(app.send_writes(self.request))
        self.assertEqual(app.QUESTS.pending_count(), 1)

    def test_refused_change_is_dropped(self):
        app.QUESTS.queue_task("pve", "not-a-task", "completed")
        self.answer = (400, b'{"success": false, "error": "Unknown task"}', {})
        app.send_writes(self.request)
        self.assertEqual(app.QUESTS.pending_count(), 0)
        self.assertIn("Unknown task", app.WRITES["error"])

    def test_refused_notice_goes_after_a_time_or_the_next_change(self):
        self.answer = (400, b'{"success": false, "error": "Unknown task"}', {})
        app.QUESTS.queue_task("pve", "not-a-task", "completed")
        app.send_writes(self.request)
        app.clear_refused(app.time.time())
        self.assertIn("Unknown task", app.WRITES["error"])          # still inside the show time
        app.clear_refused(app.time.time() + app.REFUSED_SHOW + 1)
        self.assertIsNone(app.WRITES["error"])                      # gone after the show time
        app.QUESTS.queue_task("pve", "not-a-task", "completed")
        app.send_writes(self.request)
        self.answer = (200, b'{"success": true}', {})
        app.QUESTS.queue_task("pve", "a", "completed")
        app.send_writes(self.request)
        self.assertIsNone(app.WRITES["error"])                      # gone with the next change
        # a fault that the user can act on stays
        app.WRITES["error"] = "TarkovTracker daily write limit reached. The changes are kept and sent later."
        app.clear_refused(app.time.time() + 1000)
        self.assertIn("limit", app.WRITES["error"])

    def test_no_token_for_the_mode_sends_nothing(self):
        app.QUESTS.queue_task("regular", "a", "completed")
        app.send_writes(self.request)
        self.assertEqual(self.calls, [])
        self.assertEqual(app.QUESTS.pending_count(), 1)

    def test_change_during_the_send_is_kept(self):
        app.QUESTS.queue_objective("pve", "o1", {"count": 3})
        def request(path, token, etag, body):
            app.QUESTS.queue_objective("pve", "o1", {"count": 4})  # a click while the write is on its way
            return self.answer
        app.send_writes(request)
        self.assertEqual(app.QUESTS.pending("pve")["objectives"], {"o1": {"count": 4}})


if __name__ == "__main__":
    unittest.main()
