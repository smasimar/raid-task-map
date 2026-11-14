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


if __name__ == "__main__":
    unittest.main()
