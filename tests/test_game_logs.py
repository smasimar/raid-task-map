"""Log reader tests. Run from the project folder:  py -3 -m unittest discover tests

tests/fixtures holds lines from a real game session (PvE, one local raid and two
online raids on Shoreline). The IDs, addresses and tokens in them are masked.
"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import game_logs  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
APP = (FIXTURES / "application_000.log").read_bytes()
NOTES = (FIXTURES / "push-notifications_000.log").read_bytes()


def line(clock, text):
    return f"2026-11-14 {clock}.000|1.3.0.2.48779|Info|application|{text}\n".encode()


def task_note(clock, kind, template):
    """Hand-written: the real session had no task message. Shape from TarkovMonitor's LogMessageTypes.cs."""
    body = {"type": "new_message", "eventId": "0", "dialogId": "0",
            "message": {"_id": "0", "uid": "0", "type": kind, "dt": 0, "text": "quest started", "templateId": template}}
    head = f"2026-11-14 {clock}.000|1.3.0.2.48779|Info|push-notifications|Got notification | ChatMessageReceived\n"
    return (head + json.dumps(body, indent=2) + "\n").encode()


def run(state, reader, data):
    events = []
    for entry in reader.feed(data):
        events += state.handle(*entry)
    return events


class Reader(unittest.TestCase):
    def test_entries_and_json(self):
        entries = game_logs.EntryReader().feed(NOTES)
        over = [e for e in entries if "UserMatchOver" in e[1]]
        self.assertEqual(len(over), 2)
        self.assertEqual(over[0][2]["shortId"], "M63BLT")
        self.assertEqual(over[0][2]["location"], "Shoreline")

    def test_data_cut_at_any_byte(self):
        whole = game_logs.EntryReader().feed(NOTES)
        for size in (1, 7, 100, 1024):
            reader, got = game_logs.EntryReader(), []
            for i in range(0, len(NOTES), size):
                got += reader.feed(NOTES[i:i + size])
            self.assertEqual(got, whole, f"chunk size {size}")

    def test_notification_waits_for_its_json(self):
        reader = game_logs.EntryReader()
        data = task_note("10:00:00", 10, "5936d90786f7742b1420ba5b 0")
        cut = data.index(b"\n") + 1
        self.assertEqual(reader.feed(data[:cut]), [])
        entries = reader.feed(data[cut:])
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0][2]["message"]["type"], 10)


class Raids(unittest.TestCase):
    def phases(self, data):
        state, reader, seen = game_logs.GameState(), game_logs.EntryReader(), []
        for entry in reader.feed(data):
            if state.handle(*entry) and (not seen or seen[-1] != state.raid["phase"]):
                seen.append(state.raid["phase"])
        return state, seen

    def test_real_session(self):
        state, seen = self.phases(APP)
        self.assertEqual(state.mode, "pve")
        # one local raid, then two online raids; each ends with the profile line
        self.assertEqual(seen, ["idle"] + ["loading", "starting", "raid", "idle"] * 3)

    def test_online_raid_details(self):
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        cut = APP.index(b"shortId: M63BLT")
        cut = APP.index(b"GameStarted", cut)
        run(state, reader, APP[:APP.index(b"\n", cut) + 1])
        r = state.raid
        self.assertEqual((r["phase"], r["scenePath"], r["location"], r["online"], r["raidId"]),
                         ("raid", "maps/shoreline_preset.bundle", "Shoreline", True, "M63BLT"))
        self.assertEqual(r["started"], game_logs.entry_time("2026-11-14", "20:15:47", "776"))

    def test_match_over_ends_the_raid(self):
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, line("20:14:38", "scene preset path:maps/shoreline_preset.bundle") + line("20:15:47", "GameStarted:1 real:1"))
        self.assertEqual(state.raid["phase"], "raid")
        events = run(state, game_logs.EntryReader(), NOTES)
        self.assertEqual(state.raid["phase"], "idle")
        self.assertIn({"type": "game"}, events)

    def test_old_match_over_does_not_end_a_later_raid(self):
        state = game_logs.GameState()
        run(state, game_logs.EntryReader(), line("23:00:00", "scene preset path:maps/woods_preset.bundle") + line("23:01:00", "GameStarted:1 real:1"))
        run(state, game_logs.EntryReader(), NOTES)  # all of these are before 23:00
        self.assertEqual(state.raid["phase"], "raid")

    def test_matching_cancelled(self):
        state = game_logs.GameState()
        run(state, game_logs.EntryReader(), line("10:00:00", "scene preset path:maps/woods_preset.bundle") + line("10:00:30", "Network game matching cancelled"))
        self.assertEqual(state.raid["phase"], "idle")

    def test_reconnect_keeps_the_start_time(self):
        status = "TRACE-NetworkGameCreate profileStatus: 'Profileid: 0, Status: Busy, RaidMode: Online, Ip: 0.0.0.0, Port: 1, Location: Woods, Sid: x, GameMode: deathmatch, shortId: ABC123'"
        state = game_logs.GameState()
        run(state, game_logs.EntryReader(), line("10:00:00", "scene preset path:maps/woods_preset.bundle") + line("10:00:20", status) + line("10:01:00", "GameStarted:1 real:1"))
        first = state.raid["started"]
        run(state, game_logs.EntryReader(), line("10:10:00", "scene preset path:maps/woods_preset.bundle") + line("10:10:20", status) + line("10:11:00", "GameStarted:1 real:1"))
        self.assertEqual(state.raid["started"], first)

    def test_stale_raid_expires(self):
        state = game_logs.GameState()
        run(state, game_logs.EntryReader(), line("10:00:00", "scene preset path:maps/woods_preset.bundle") + line("10:01:00", "GameStarted:1 real:1"))
        self.assertFalse(state.expire(state.raid["started"] + 60))
        self.assertTrue(state.expire(state.raid["started"] + game_logs.MAX_RAID_SECONDS + 1))
        self.assertEqual(state.raid["phase"], "idle")

    def test_session_modes(self):
        for raw, mode in (("Pve", "pve"), ("Regular", "regular"), ("PvpSeason", "pvp-season"), ("Other", None)):
            state = game_logs.GameState()
            run(state, game_logs.EntryReader(), line("10:00:00", f"Session mode: {raw}"))
            self.assertEqual(state.mode, mode)


class Tasks(unittest.TestCase):
    def test_task_messages(self):
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        data = (task_note("10:00:00", 10, "5936d90786f7742b1420ba5b 0") + task_note("10:05:00", 12, "5936d90786f7742b1420ba5b 0")
                + task_note("10:06:00", 11, "59674cd986f7744ab26e32f2 0") + line("10:07:00", "x"))
        events = [e for e in run(state, reader, data) if e["type"] == "task"]
        self.assertEqual([(e["status"], e["id"]) for e in events],
                         [("started", "5936d90786f7742b1420ba5b"), ("finished", "5936d90786f7742b1420ba5b"), ("failed", "59674cd986f7744ab26e32f2")])

    def test_other_messages_are_not_tasks(self):
        events = run(game_logs.GameState(), game_logs.EntryReader(), NOTES)  # the real file has two type-2 messages
        self.assertEqual([e for e in events if e["type"] == "task"], [])


class Folders(unittest.TestCase):
    def test_newest_log_folder(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            for name in ("log_2026.11.13_21-09-56_1.3.0.2.48779", "log_2026.11.14_10-17-53_1.3.0.2.48779", "other"):
                os.mkdir(os.path.join(d, name))
            self.assertTrue(game_logs.newest_log_folder(d).endswith("log_2026.11.14_10-17-53_1.3.0.2.48779"))
            self.assertIsNone(game_logs.newest_log_folder(os.path.join(d, "missing")))

    def test_follower_reads_only_new_bytes(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            app = os.path.join(d, "2026.11.14 application_000.log")
            with open(app, "wb") as f:
                f.write(line("10:00:00", "Session mode: Pve"))
            follower = game_logs.LogFollower(d)
            self.assertEqual(len(follower.read()), 1)
            self.assertEqual(follower.read(), [])
            with open(app, "ab") as f:
                f.write(line("10:00:05", "scene preset path:maps/woods_preset.bundle"))
            with open(os.path.join(d, "2026.11.14 push-notifications_000.log"), "wb") as f:
                f.write(NOTES)
            self.assertEqual(len([e for e in follower.read() if "UserMatchOver" in e[1]]), 2)


if __name__ == "__main__":
    unittest.main()
