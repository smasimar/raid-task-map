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
        self.assertEqual(r["side"], "pmc")

    STATUS = "TRACE-NetworkGameCreate profileStatus: 'Profileid: {}, Status: Busy, RaidMode: Online, Ip: 0.0.0.0, Port: 1, Location: Woods, Sid: x, GameMode: deathmatch, shortId: {}'"

    def side(self, lines):
        state = game_logs.GameState()
        run(state, game_logs.EntryReader(), b"".join(lines))
        return state.raid["side"]

    def test_scav_raid_uses_a_different_profile(self):
        menu = line("09:59:00", "SelectProfile ProfileId:aaaa AccountId:1")
        load = line("10:00:00", "scene preset path:maps/woods_preset.bundle")
        go = line("10:01:00", "GameStarting:1 real:1") + line("10:01:12", "GameStarted:1 real:1")
        self.assertEqual(self.side([menu, load, line("10:00:20", self.STATUS.format("aaaa", "ABC123")), go]), "pmc")
        self.assertEqual(self.side([menu, load, line("10:00:20", self.STATUS.format("bbbb", "ABC124")), go]), "scav")

    def test_side_from_the_countdown_when_the_profile_is_not_known(self):
        load = line("10:00:00", "scene preset path:maps/woods_preset.bundle") + line("10:00:20", self.STATUS.format("bbbb", "ABC125"))
        self.assertEqual(self.side([load, line("10:01:00", "GameStarting:1 real:1"), line("10:01:12", "GameStarted:1 real:1")]), "pmc")
        self.assertEqual(self.side([load, line("10:01:00", "GameStarting:1 real:1"), line("10:01:00", "GameStarted:1 real:1")]), "scav")
        self.assertEqual(self.side([load, line("10:01:00", "GameStarted:1 real:1")]), "scav")

    BACKEND = "2026-11-14 {}.000|1.3.0.2.48779|Info|backend|---> Request HTTPS, id [12]: URL: https://gw-pve.example.com{}. \n"

    def test_insurance_request_tells_pmc_from_scav_in_a_local_raid(self):
        load = line("10:00:30", "scene preset path:maps/woods_preset.bundle")
        go = line("10:01:00", "GameStarting:1 real:1") + line("10:01:00", "GameStarted:1 real:1")
        back = line("10:20:00", "PrepareSelectedProfileLocally ProfileId:aaaa AccountId:1")
        insurance = self.BACKEND.format("10:00:10", game_logs.INSURANCE_REQUEST).encode()
        other = self.BACKEND.format("10:00:10", "/client/raid/configuration").encode()
        self.assertEqual(self.side([insurance, load, go]), "pmc")
        self.assertEqual(self.side([other, load, go]), "scav")
        # the request of one raid does not count for the next raid
        again = line("10:30:30", "scene preset path:maps/woods_preset.bundle") + line("10:31:00", "GameStarted:1 real:1")
        self.assertEqual(self.side([insurance, load, go, back, self.BACKEND.format("10:30:00", "/client/raid/configuration").encode(), again]), "scav")

    def test_transit_keeps_the_side(self):
        """Real PvE logs: a PMC raid on Customs, then a transit to Factory. The game selects the profile
        again at the transit and asks for no insurance, which looked like a Scav raid."""
        insurance = self.BACKEND.format("00:42:57", game_logs.INSURANCE_REQUEST).encode()
        customs = (line("00:43:09", "scene preset path:maps/customs_preset.bundle rcid:bigmap.scenespreset.asset")
                   + line("00:43:33", "[Transit] Flag:Common, RaidId:6b00db247b7c40f9bb0d80d6, Count:0, Locations:bigmap -> ")
                   + line("00:44:06", "GameStarting:44.51(0) real:57.73(0) diff:13.22") + line("00:44:06", "GameStarted:44.51(0) real:57.73(0) diff:13.22"))
        back = line("01:02:13", "PrepareSelectedProfileLocally ProfileId:aaaa AccountId:1")
        hop = line("01:02:14", "PVE transit hop local:True location:factory4_day side:Pmc onlineToggle:False cachedMode:Local")
        factory = (line("01:02:15", "scene preset path:maps/factory_day_preset.bundle rcid:factory_day.scenespreset.asset")
                   + line("01:02:25", "[Transit] Flag:Common, RaidId:6b00db247b7c40f9bb0d80d6, Count:1, Locations:bigmap -> factory4_day -> ")
                   + line("01:02:46", "GameStarting:23.23(0) real:32.37(0) diff:9.13") + line("01:02:46", "GameStarted:23.23(0) real:32.37(0) diff:9.13"))
        noise = self.BACKEND.format("01:02:20", "/client/raid/configuration").encode()
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, insurance + customs)
        self.assertEqual((state.raid["side"], state.raid["transits"]), ("pmc", 0))
        run(state, reader, back + hop + noise + factory)
        self.assertEqual((state.raid["side"], state.raid["transits"], state.raid["scenePath"]), ("pmc", 1, "maps/factory_day_preset.bundle"))
        # without the hop line, the side comes from the first map of the same raid id
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, insurance + customs + back + noise + factory)
        self.assertEqual(state.raid["side"], "pmc")
        # a Scav raid that transits stays a Scav raid
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, self.BACKEND.format("00:42:57", "/client/raid/configuration").encode() + customs + back + noise + factory)
        self.assertEqual(state.raid["side"], "scav")
        # a new raid (Count:0) does not take the side of the last one
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        again = (line("02:00:00", "scene preset path:maps/woods_preset.bundle")
                 + line("02:00:10", "[Transit] Flag:Common, RaidId:ffff, Count:0, Locations:woods -> ") + line("02:00:30", "GameStarted:1 real:1"))
        run(state, reader, insurance + customs + back + self.BACKEND.format("01:59:00", "/client/raid/configuration").encode() + again)
        self.assertEqual(state.raid["side"], "scav")

    def test_transit_to_an_online_map_keeps_the_side(self):
        """Real PvE logs: a PMC raid on Ground Zero 21+ (local), then a transit to Streets (online).
        No "transit hop" line comes; a "Transit reconnect" line comes before the map loads, and the
        [Transit] line only after GameStarted."""
        insurance = self.BACKEND.format("23:57:50", game_logs.INSURANCE_REQUEST).encode()
        gz = (line("23:58:05", "scene preset path:maps/sandbox_high_preset.bundle rcid:sandbox_high.scenespreset.asset")
              + line("23:58:21", "[Transit] Flag:Common, RaidId:6b07680c499efc4f210ec3ff, Count:0, Locations:Sandbox_high -> ")
              + line("23:58:47", "GameStarted:29.73(0) real:42.72(0) diff:12.99") + line("23:58:47", "GameStarting:29.73(0) real:42.72(0) diff:12.99"))
        back = line("23:59:15", "PrepareSelectedProfileLocally ProfileId:aaaa AccountId:1")
        reconnect = line("23:59:16", "Transit reconnect status:Busy raidMode:Online location:TarkovStreets settingsLocal:False")
        streets = (line("23:59:16", "scene preset path:maps/city_preset.bundle rcid:city.scenespreset.asset")
                   + line("23:59:24", "TRACE-NetworkGameCreate profileStatus: 'Profileid: aaaa, Status: Busy, RaidMode: Online, Ip: 1.2.3.4, Port: 17004, Location: TarkovStreets, Sid: fr")
                   + line("23:59:40", "GameStarting:33.64(0.63) real:46.61(2.99) diff:12.97") + line("23:59:52", "GameStarted:44.64(11) real:58.65(12.04) diff:14.01"))
        late = line("23:59:53", "[Transit] `aaaa` Count:1, EventPlayer:False")
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, insurance + gz)
        self.assertEqual(state.raid["side"], "pmc")
        run(state, reader, back + reconnect + streets + late)
        self.assertEqual((state.raid["side"], state.raid["transits"], state.raid["scenePath"]), ("pmc", 1, "maps/city_preset.bundle"))
        # without the reconnect line, the late [Transit] line puts the side right
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, insurance + gz + back + streets)
        self.assertEqual(state.raid["side"], "scav")
        run(state, reader, late)
        self.assertEqual((state.raid["side"], state.raid["transits"]), ("pmc", 1))
        # a Scav raid that transits to an online map stays a Scav raid
        state, reader = game_logs.GameState(), game_logs.EntryReader()
        run(state, reader, self.BACKEND.format("23:57:50", "/client/raid/configuration").encode() + gz + back + reconnect + streets + late)
        self.assertEqual(state.raid["side"], "scav")

    def test_follower_puts_the_three_logs_in_time_order(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "x application_000.log"), "wb") as f:
                f.write(line("10:00:30", "scene preset path:maps/woods_preset.bundle") + line("10:01:00", "GameStarted:1 real:1"))
            with open(os.path.join(d, "x backend_000.log"), "wb") as f:
                f.write(self.BACKEND.format("10:00:10", game_logs.INSURANCE_REQUEST).encode())
            state = game_logs.GameState()
            for entry in game_logs.LogFollower(d).read():
                state.handle(*entry)
            self.assertEqual(state.raid["side"], "pmc")

    def test_local_raid_has_no_side_without_the_backend_log(self):
        self.assertIsNone(self.side([line("10:00:00", "scene preset path:maps/woods_preset.bundle"),
                                     line("10:01:00", "GameStarting:1 real:1"), line("10:01:00", "GameStarted:1 real:1")]))

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


    def test_real_task_message(self):
        data = (FIXTURES / "task-messages.log").read_bytes() + line("21:43:00", "x")
        state = game_logs.GameState()
        run(state, game_logs.EntryReader(), line("21:36:00", "Session mode: Pve"))
        events = [e for e in run(state, game_logs.EntryReader(), data) if e["type"] == "task"]
        self.assertEqual([(e["status"], e["id"], e["mode"]) for e in events], [("started", "657315ddab5a49b71f098853", "pve")])

    def test_net_changes(self):
        ev = lambda mode, status, task: {"mode": mode, "status": status, "id": task}
        changes = game_logs.net_task_changes([ev("pve", "started", "a"), ev("pve", "started", "b"), ev("pve", "finished", "a"),
                                              ev("regular", "started", "a"), ev("pve", "failed", "c"), ev("pve", "started", "c")])
        self.assertEqual(changes, {"pve": {"started": ["b", "c"], "ended": ["a"]}, "regular": {"started": ["a"], "ended": []}})


class Folders(unittest.TestCase):
    def test_folders_sort_by_time_not_by_text(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            for name in ("log_2026.02.26_10-03-18_1.0.2.0.43037", "log_2026.02.26_9-03-18_1.0.2.0.43037"):
                os.mkdir(os.path.join(d, name))
            self.assertTrue(game_logs.newest_log_folder(d).endswith("log_2026.02.26_10-03-18_1.0.2.0.43037"))

    def test_task_events_of_all_sessions(self):
        import tempfile, os
        with tempfile.TemporaryDirectory() as d:
            for name, mode, kind in (("log_2026.11.13_9-00-00_1", "Pve", 10), ("log_2026.11.14_10-00-00_1", "Regular", 12)):
                os.mkdir(os.path.join(d, name))
                with open(os.path.join(d, name, "x application_000.log"), "wb") as f:
                    f.write(line("09:00:00", f"Session mode: {mode}"))
                with open(os.path.join(d, name, "x push-notifications_000.log"), "wb") as f:
                    f.write(task_note("09:30:00", kind, "aaaaaaaaaaaaaaaaaaaaaaaa 0"))
            events = game_logs.task_events(d)
            self.assertEqual([(e["mode"], e["status"]) for e in events], [("pve", "started"), ("regular", "finished")])
            self.assertEqual(game_logs.task_events(d, after=events[-1]["time"]), [])

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
