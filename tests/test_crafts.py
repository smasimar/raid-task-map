import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import crafts  # noqa: E402

FILES = {
    "crafts": {"data": [{"id": "c1", "station": "st1", "level": 1, "duration": 60,
                         "requiredItems": [{"item": "a", "count": 2, "attributes": {}}],
                         "productItem": {"item": "p", "count": 1, "attributes": {}}}]},
    "hideout": {"data": {"st1": {"id": "st1", "name": "area_10", "normalizedName": "workbench", "imageLink": "w.png", "levels": [1, 2]}}},
    "hideout_en": {"data": {"area_10": "Workbench"}},
    "items": {"data": {"fleaMarket": {"sellOfferFeeRate": 0.05, "sellRequirementFeeRate": 0.05, "reputationLevels": []}, "items": {
        "a": {"id": "a", "avg24hPrice": 100, "lastLowPrice": 90, "basePrice": 50, "types": [],
              "buyFromTrader": [{"trader": "t1", "priceRUB": 120, "minTraderLevel": 2, "buyLimit": 5}, {"trader": "t2", "priceRUB": 80, "minTraderLevel": 1}],
              "sellToTrader": []},
        "p": {"id": "p", "avg24hPrice": 0, "basePrice": 400, "types": ["noFlea"], "iconLink": "p.webp",
              "buyFromTrader": [], "sellToTrader": [{"trader": "t1", "priceRUB": 10}, {"trader": "t2", "priceRUB": 30}]},
        "other": {"id": "other", "avg24hPrice": 5, "basePrice": 1, "types": []},
    }}},
}


class Fetch:
    def __init__(self):
        self.calls = 0
        self.fail = False

    def __call__(self, url):
        if self.fail:
            raise OSError("offline")
        self.calls += 1
        return json.loads(json.dumps(FILES[url.rsplit("/", 1)[1]]))


class CraftCacheTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name) / "cache"
        self.fetch = Fetch()

    def tearDown(self):
        self.tmp.cleanup()

    def test_keeps_only_the_prices_of_craft_items(self):
        d = crafts.CraftCache(self.dir, self.fetch).get("pve")
        self.assertEqual(set(d["prices"]), {"a", "p"})
        self.assertEqual(d["prices"]["a"]["buy"], {"trader": "t2", "priceRUB": 80, "minTraderLevel": 1}, "the cheapest trader offer")
        self.assertEqual(d["prices"]["p"]["sell"], {"trader": "t2", "priceRUB": 30}, "the best trader sale")
        self.assertTrue(d["prices"]["p"]["noFlea"])
        self.assertEqual(d["stations"]["st1"], {"id": "st1", "name": "area_10", "normalizedName": "workbench", "imageLink": "w.png"})
        self.assertEqual(d["flea"], {"sellOfferFeeRate": 0.05, "sellRequirementFeeRate": 0.05})

    def test_saved_data_is_used_until_it_is_old(self):
        c = crafts.CraftCache(self.dir, self.fetch, max_age=100)
        c.get("pve")
        self.assertEqual(self.fetch.calls, 4)
        c.get("pve")
        self.assertEqual(self.fetch.calls, 4, "no download from memory")
        c2 = crafts.CraftCache(self.dir, self.fetch, max_age=100)
        self.assertEqual(c2.get("pve")["prices"]["a"]["avg"], 100)
        self.assertEqual(self.fetch.calls, 4, "a restart of the app uses the saved file")
        c2.get("pve", force=True)
        self.assertEqual(self.fetch.calls, 8, "force downloads again")
        c2.mem["pve"]["fetched"] = time.time() - 200
        c2.get("pve")
        self.assertEqual(self.fetch.calls, 12, "old data is downloaded again")
        c2.get("regular")
        self.assertEqual(self.fetch.calls, 16, "each game mode has its own data")

    def test_a_failed_download_gives_the_old_data(self):
        c = crafts.CraftCache(self.dir, self.fetch)
        c.get("pve")
        self.fetch.fail = True
        d = c.get("pve", force=True)
        self.assertTrue(d["stale"])
        self.assertEqual(d["prices"]["a"]["avg"], 100)
        st = c.status("pve")
        self.assertEqual((st["items"], st["crafts"], st["error"], st["busy"]), (2, 1, "offline", False))
        with self.assertRaises(OSError):
            c.get("regular")
        self.assertNotIn("fetched", c.status("regular"), "no saved data for this mode")
        self.fetch.fail = False
        c.get("pve", force=True)
        self.assertIsNone(c.status("pve")["error"], "a good download clears the error")

    def test_saved_for_8_hours(self):
        self.assertEqual(crafts.MAX_AGE, 8 * 3600)


if __name__ == "__main__":
    unittest.main()
