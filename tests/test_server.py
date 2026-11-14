"""Server unit tests. Run from the project folder:  py -3 -m unittest discover tests"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tarkov_quest_map as tqm  # noqa: E402


class ParseScreenshot(unittest.TestCase):
    def test_normal_name(self):
        pos = tqm.parse_screenshot("2024-08-13[22-41]_351.48, 1.07, 73.79_0.0, -0.9, 0.0, 0.4_13.27 (0).png")
        self.assertEqual((pos["x"], pos["y"], pos["z"]), (351.48, 1.07, 73.79))
        self.assertAlmostEqual(pos["rotation"], -130.73, places=1)

    def test_screenshot_number_above_9(self):
        pos = tqm.parse_screenshot("2024-08-13[22-41]_-351.48, -1.07, 73.79_0.00000, -0.98765, 0.0, 0.4_13.27 (12).png")
        self.assertEqual(pos["x"], -351.48)

    def test_exponent_quaternion(self):
        self.assertIsNotNone(
            tqm.parse_screenshot("2024-08-13[22-41]_351.48, 1.07, 73.79_1E-05, -0.9, 0.0, 0.4_13.27 (1).png"))

    def test_other_files(self):
        self.assertIsNone(tqm.parse_screenshot("holiday.png"))
        self.assertIsNone(tqm.parse_screenshot("2024-08-13[22-41]_no position (0).png"))


class RequestAllowed(unittest.TestCase):
    def test_local(self):
        self.assertTrue(tqm.request_allowed("localhost:3000", ""))
        self.assertTrue(tqm.request_allowed("127.0.0.1:3000", "http://localhost:3000"))
        self.assertTrue(tqm.request_allowed("[::1]:3000", "http://[::1]:3000"))

    def test_foreign(self):
        self.assertFalse(tqm.request_allowed("evil.example:3000", ""))          # DNS rebinding
        self.assertFalse(tqm.request_allowed("localhost:3000", "https://evil.example"))  # cross-site POST
        self.assertFalse(tqm.request_allowed("localhost:3000", "null"))
        self.assertFalse(tqm.request_allowed("", ""))


class GameMode(unittest.TestCase):
    def test_prefix(self):
        self.assertEqual(tqm.game_mode_for_token("PVE_abc"), "pve")
        self.assertEqual(tqm.game_mode_for_token("SZN_abc"), "pvp-season")
        self.assertEqual(tqm.game_mode_for_token("PVP_abc"), "regular")


class Quests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.dir = tempfile.TemporaryDirectory()
        self.path = Path(self.dir.name) / "state.json"
        self.events = []
        self.q = tqm.QuestList(self.path, self.events.append)

    def tearDown(self):
        self.dir.cleanup()

    def test_add_remove_and_reload(self):
        self.q.apply("pve", add=["a", "b", "a"], add_custom=["New Quest"])
        self.q.apply("pve", remove=["a"], add_custom=["new quest"])
        self.q.apply("regular", add=["z"])
        again = tqm.QuestList(self.path).public()
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
        self.assertEqual(tqm.QuestList(self.path).log_time(), 300.0)

    def test_migrated_flag(self):
        self.q.apply("pve", add=["a"], migrated=True)
        self.assertEqual(self.q.public()["migrated"], ["pve"])


class Tokens(unittest.TestCase):
    def test_old_single_token_moves_to_its_mode(self):
        import json, tempfile
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "config.json"
            path.write_text(json.dumps({"token": "PVE_abcdefghijkl"}), encoding="utf-8")
            real, tqm.CONFIG_PATH = tqm.CONFIG_PATH, path
            try:
                cfg = tqm.load_config()
            finally:
                tqm.CONFIG_PATH = real
        self.assertEqual(cfg["tokens"], {"pve": "PVE_abcdefghijkl"})
        self.assertNotIn("token", cfg)
        self.assertFalse(cfg["writeTT"])


class Overlay(unittest.TestCase):
    BODY = b'{"data": {"tasksProgress": [{"id": "a", "complete": false}], "taskObjectivesProgress": [{"id": "o1", "complete": false, "count": 2}]}}'

    def test_nothing_pending_keeps_the_bytes(self):
        self.assertIs(tqm.overlay_progress(self.BODY, {"tasks": {}, "objectives": {}}), self.BODY)

    def test_pending_changes_show(self):
        import json
        out = json.loads(tqm.overlay_progress(self.BODY, {"tasks": {"a": "completed", "b": "failed"},
                                                         "objectives": {"o1": {"count": 5}, "o2": {"state": "completed"}}}))["data"]
        self.assertEqual(out["tasksProgress"], [{"id": "a", "complete": True, "failed": False}, {"id": "b", "complete": False, "failed": True}])
        self.assertEqual(out["taskObjectivesProgress"], [{"id": "o1", "complete": False, "count": 5}, {"id": "o2", "complete": True}])


class Writes(unittest.TestCase):
    """send_writes with a stand-in for TarkovTracker."""

    def setUp(self):
        import tempfile
        self.dir = tempfile.TemporaryDirectory()
        self.saved = (tqm.QUESTS, dict(tqm.CONFIG), dict(tqm.WRITES))
        tqm.QUESTS = tqm.QuestList(Path(self.dir.name) / "state.json")
        tqm.CONFIG.clear()
        tqm.CONFIG.update({"tokens": {"pve": "PVE_testtoken0001"}, "mode": "pve", "writeTT": True})
        self.calls = []
        self.answer = (200, b'{"success": true}', {"X-RateLimit-Remaining": "97"})

    def tearDown(self):
        tqm.QUESTS = self.saved[0]
        tqm.CONFIG.clear(); tqm.CONFIG.update(self.saved[1])
        tqm.WRITES.clear(); tqm.WRITES.update(self.saved[2])
        self.dir.cleanup()

    def request(self, path, token, etag, body):
        self.calls.append((path, body))
        if isinstance(self.answer, Exception):
            raise self.answer
        return self.answer

    def test_fast_clicks_on_one_step_make_one_write(self):
        for n in range(1, 11):
            tqm.QUESTS.queue_objective("pve", "o1", {"count": n, "state": "uncompleted"})
        self.assertTrue(tqm.send_writes(self.request))
        self.assertEqual(self.calls, [("/progress/task/objective/o1", {"count": 10, "state": "uncompleted"})])
        self.assertEqual(tqm.QUESTS.pending_count(), 0)
        self.assertEqual(tqm.WRITES["remaining"], "97")

    def test_one_task_and_many_tasks(self):
        tqm.QUESTS.queue_task("pve", "a", "completed")
        tqm.send_writes(self.request)
        tqm.QUESTS.queue_task("pve", "a", "uncompleted")
        tqm.QUESTS.queue_task("pve", "b", "failed")
        tqm.send_writes(self.request)
        self.assertEqual(self.calls, [("/progress/task/a", {"state": "completed"}),
                                      ("/progress/tasks", [{"id": "a", "state": "uncompleted"}, {"id": "b", "state": "failed"}])])

    def test_limit_reached_keeps_the_queue(self):
        tqm.QUESTS.queue_task("pve", "a", "completed")
        self.answer = (429, b'{"success": false, "error": "quota"}', {"Retry-After": "120"})
        self.assertFalse(tqm.send_writes(self.request))
        self.assertEqual(tqm.QUESTS.pending("pve")["tasks"], {"a": "completed"})
        self.assertGreater(tqm.WRITES["retryAt"], tqm.time.time() + 100)
        self.assertIn("limit", tqm.WRITES["error"])
        # the queue is on disk, so it is still there after a restart
        self.assertEqual(tqm.QuestList(tqm.QUESTS.path).pending("pve")["tasks"], {"a": "completed"})

    def test_network_fault_keeps_the_queue(self):
        tqm.QUESTS.queue_task("pve", "a", "completed")
        self.answer = OSError("offline")
        self.assertFalse(tqm.send_writes(self.request))
        self.assertEqual(tqm.QUESTS.pending_count(), 1)

    def test_refused_change_is_dropped(self):
        tqm.QUESTS.queue_task("pve", "not-a-task", "completed")
        self.answer = (400, b'{"success": false, "error": "Unknown task"}', {})
        tqm.send_writes(self.request)
        self.assertEqual(tqm.QUESTS.pending_count(), 0)
        self.assertIn("Unknown task", tqm.WRITES["error"])

    def test_no_token_for_the_mode_sends_nothing(self):
        tqm.QUESTS.queue_task("regular", "a", "completed")
        tqm.send_writes(self.request)
        self.assertEqual(self.calls, [])
        self.assertEqual(tqm.QUESTS.pending_count(), 1)

    def test_change_during_the_send_is_kept(self):
        tqm.QUESTS.queue_objective("pve", "o1", {"count": 3})
        def request(path, token, etag, body):
            tqm.QUESTS.queue_objective("pve", "o1", {"count": 4})  # a click while the write is on its way
            return self.answer
        tqm.send_writes(request)
        self.assertEqual(tqm.QUESTS.pending("pve")["objectives"], {"o1": {"count": 4}})


if __name__ == "__main__":
    unittest.main()
