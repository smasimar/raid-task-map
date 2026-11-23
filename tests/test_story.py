import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import crafts  # noqa: E402
import story  # noqa: E402

T = "@tt:overlay:/storyChapters"
EDITIONS = {"data": {"storyChapters": [
    {"id": "two", "name": f"{T}/two/name", "order": 2, "wikiLink": f"{T}/two/wikiLink", "chapterQuestId": "q2",
     "chapterRequirements": [{"id": "one", "name": f"{T}/two/req"}], "mutuallyExclusiveQuestPairs": [["sa", "sb"]],
     "endings": [{"id": "e1", "systemName": "EscapedFromTarkov"}],
     "objectives": {"x": {"id": "x", "order": 1, "description": f"{T}/two/x", "type": "main", "sourceQuestId": "sa"}}},
    {"id": "one", "name": f"{T}/one/name", "order": 1, "wikiLink": f"{T}/one/wikiLink", "autoStart": True,
     "rewards": {"description": f"{T}/one/reward"}, "mapUnlocks": [{"id": "m1", "name": f"{T}/one/m1"}],
     "objectives": {
         "a": {"id": "a", "order": 1, "description": f"{T}/one/a", "type": "main", "sourceQuestId": "s1", "completionPolicy": "tutorial",
               "unlocks": [{"type": "trader", "id": "t1", "name": f"{T}/one/a/t1", "note": f"{T}/one/a/t1/note"}]},
         "b": {"id": "b", "order": 2, "description": f"{T}/one/b", "type": "main", "sourceQuestId": "s2"},
         "c": {"id": "c", "order": 3, "description": f"{T}/one/c", "type": "optional", "sourceQuestId": "s2", "parentObjectiveId": "b"},
         "d": {"id": "d", "order": 4, "description": f"{T}/one/d", "type": "main", "sourceQuestId": "s3"},
     }},
]}}
STRINGS = {"data": {"strings": {
    f"{T}/one/name": "Tour", f"{T}/one/wikiLink": "https://wiki.test/wiki/Tour", f"{T}/one/reward": "An achievement",
    f"{T}/one/m1": "Customs", f"{T}/one/a": "Escape Ground Zero", f"{T}/one/a/t1": "Therapist", f"{T}/one/a/t1/note": "After the escape",
    f"{T}/one/b": "Locate the fallen plane", f"{T}/one/c": "Collect the cash", f"{T}/one/d": "Something else entirely",
    f"{T}/two/name": "Falling Skies", f"{T}/two/wikiLink": "https://wiki.test/wiki/Falling_Skies", f"{T}/two/req": "Tour",
    f"{T}/two/x": "Talk to Prapor",
}}}
SECTIONS = {"Tour": [{"level": "2", "anchor": "Guide", "line": "Guide"},
                     {"level": "3", "anchor": "Locate_the_fallen_plane", "line": "Locate the fallen plane"},
                     {"level": "3", "anchor": "Rewards", "line": "Rewards"}]}


def fetch(url):
    if "/editions" in url:
        return EDITIONS
    if "/strings" in url:
        return STRINGS
    page = url.rsplit("page=", 1)[1]
    if page not in SECTIONS:
        raise OSError("wiki is down")
    return {"parse": {"sections": SECTIONS[page]}}


class LinkTest(unittest.TestCase):
    def test_close_heading_and_stage(self):
        steps = [{"id": "1", "text": "Locate the fallen plane", "stage": "s"},
                 {"id": "2", "text": "Collect the cash", "stage": "s"},
                 {"id": "3", "text": "Hand over the cash to Therapist", "stage": "t"},
                 {"id": "4", "text": "Talk to Ragman", "stage": "u"}]
        secs = [("Locate_the_fallen_plane", "Locate the fallen plane"), ("Hand_cash", "(<i>Optional</i>) Hand over 2,000 USD to Therapist"),
                ("Ragman", "Ragman - Interchange")]
        links = story.link_steps(steps, secs)
        self.assertEqual(links["1"], "Locate_the_fallen_plane")
        self.assertEqual(links["2"], "Locate_the_fallen_plane", "a step with no close heading takes the heading of its stage")
        self.assertEqual(links["3"], "Hand_cash", "markup in a heading is ignored")
        self.assertNotIn("4", links, "one shared word of two is not enough")


class BuildTest(unittest.TestCase):
    def test_build(self):
        d = story.build("pve", fetch)
        self.assertEqual([c["name"] for c in d["chapters"]], ["Tour", "Falling Skies"], "chapters in order, with their text")
        one, two = d["chapters"]
        self.assertEqual((one["autoStart"], one["rewards"], one["unlocks"]), (True, "An achievement", [{"type": "map", "id": "m1", "name": "Customs", "note": None}]))
        a, b, c, dd = one["steps"]
        self.assertTrue(a["tutorial"] and not a["optional"])
        self.assertEqual(a["unlocks"], [{"type": "trader", "id": "t1", "name": "Therapist", "note": "After the escape"}])
        self.assertEqual(b["wiki"], "https://wiki.test/wiki/Tour#Locate_the_fallen_plane")
        self.assertEqual((c["optional"], c["parent"], c["wiki"]), (True, "b", b["wiki"]), "an optional step under its parent, with the link of its stage")
        self.assertEqual(dd["wiki"], "https://wiki.test/wiki/Tour", "no close heading: the chapter page")
        self.assertEqual(two["requires"], [{"id": "one", "name": "Tour"}])
        self.assertEqual((two["exclusive"], two["endings"]), ([["sa", "sb"]], [{"id": "e1", "name": "EscapedFromTarkov"}]))
        self.assertEqual(two["steps"][0]["wiki"], "https://wiki.test/wiki/Falling_Skies", "a wiki failure gives the chapter page")

    def test_cache(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = crafts.CraftCache(Path(tmp), fetch=fetch, max_age=story.MAX_AGE, build=story.build, name="story")
            c.get("pve")
            self.assertTrue((Path(tmp) / "story-pve.json").exists(), "saved in its own file")
            st = c.status("pve")
            self.assertEqual((st["chapters"], st["steps"]), (2, 5))
        self.assertEqual(story.MAX_AGE, 24 * 3600)



class RoutesTest(unittest.TestCase):
    def test_real_file(self):
        r = story.routes()
        self.assertEqual(r["chapter"], "the-ticket")
        self.assertEqual([x["name"] for x in r["routes"]], ["Survivor", "Savior", "Debtor", "Fallen"])
        steps = [st for sec in r["sections"].values() for st in sec["steps"]]
        self.assertTrue(all(("mark" in st) == (st.get("kind") != "note") for st in steps), "every step that can be marked has a mark id")
        self.assertTrue(all(st["mark"] == st.get("ref", st.get("id")) for st in steps if "mark" in st))
        self.assertTrue(all(st["text"] for st in steps), "escape steps get the escape text")
        self.assertEqual({st["when"] for st in steps if "when" in st}, {"A", "B"})
        ids = [st["id"] for st in steps if "id" in st]
        self.assertEqual(len(ids), len(set(ids)), "custom step ids are unique")

    def test_broken_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "r.json"
            bad.write_text('{"sections": {}, "routes": [{"id": "x", "sections": ["missing"]}]}', encoding="utf-8")
            self.assertIsNone(story.routes(bad))
            self.assertIsNone(story.routes(Path(tmp) / "none.json"))


if __name__ == "__main__":
    unittest.main()
