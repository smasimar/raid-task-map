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


if __name__ == "__main__":
    unittest.main()
