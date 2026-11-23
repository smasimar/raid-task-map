"""Hideout crafts and item prices from json.tarkov.dev, kept on disk for a time.

The item file of tarkov.dev is large (about 17 MB, 2 MB compressed). The page needs only the prices of
the items that crafts use or make, so this module downloads the files, keeps those prices, and saves
the result in the cache folder. The flea prices are 24-hour averages and change slowly, so the saved
data is used again until it is MAX_AGE seconds old. The Settings tab can start a new download.

Raid Task Map is free software under the GNU General Public License, version 3.
"""
import gzip
import json
import threading
import time
import urllib.request
from pathlib import Path

JSON_API = "https://json.tarkov.dev"
MAX_AGE = 8 * 3600      # seconds that saved prices are used before a new download
USER_AGENT = "RaidTaskMap/1.0 (local)"


def fetch_json(url: str):
    """GET a JSON file. The answer is asked for in gzip form, which is much smaller."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            body = gzip.decompress(body)
    return json.loads(body)


def _offer(o, keys):
    return {k: o.get(k) for k in keys if o.get(k) is not None}


def build(mode: str, fetch=fetch_json) -> dict:
    """Download the crafts, the hideout stations and the item prices for one game mode."""
    base = f"{JSON_API}/{mode}"
    crafts = fetch(f"{base}/crafts").get("data") or []
    hideout = fetch(f"{base}/hideout").get("data") or {}
    try:
        hideout_en = fetch(f"{base}/hideout_en").get("data") or {}
    except Exception:
        hideout_en = {}
    items = fetch(f"{base}/items").get("data") or {}
    used = set()
    for c in crafts:
        used.add(c["productItem"]["item"])
        used.update(r["item"] for r in c.get("requiredItems", []))
    prices = {}
    for item_id in used:
        it = (items.get("items") or {}).get(item_id)
        if not it:
            continue
        buy = sorted((o for o in it.get("buyFromTrader") or [] if (o.get("priceRUB") or 0) > 0), key=lambda o: o["priceRUB"])
        sell = sorted((o for o in it.get("sellToTrader") or [] if (o.get("priceRUB") or 0) > 0), key=lambda o: -o["priceRUB"])
        prices[item_id] = {
            "avg": it.get("avg24hPrice") or 0, "low": it.get("lastLowPrice") or 0, "base": it.get("basePrice") or 0,
            "noFlea": "noFlea" in (it.get("types") or []), "icon": it.get("iconLink"),
            "buy": _offer(buy[0], ("trader", "priceRUB", "minTraderLevel")) if buy else None,
            "sell": _offer(sell[0], ("trader", "priceRUB")) if sell else None,
        }
    flea = items.get("fleaMarket") or {}
    return {
        "mode": mode, "fetched": time.time(), "crafts": crafts,
        "stations": {k: {f: s.get(f) for f in ("id", "name", "normalizedName", "imageLink")} for k, s in hideout.items()},
        "stationsEn": hideout_en, "prices": prices,
        "flea": {k: flea.get(k) for k in ("sellOfferFeeRate", "sellRequirementFeeRate") if k in flea},
    }


class CraftCache:
    """The data of each game mode, in memory and in a file in the cache folder.

    build(mode, fetch) makes the data; the default is the crafts. story.py uses the same cache
    for the story chapters, with a different build and file name."""

    def __init__(self, folder: Path, fetch=fetch_json, max_age: int = MAX_AGE, build=None, name: str = "crafts"):
        self.folder = Path(folder)
        self.fetch = fetch
        self.max_age = max_age
        self.build = build or globals()["build"]
        self.name = name
        self.mem = {}
        self.locks = {}
        self.busy = set()     # game modes that are downloading now
        self.errors = {}      # game mode -> (time, text) of the last failed download
        self.lock = threading.Lock()

    def _path(self, mode: str) -> Path:
        return self.folder / f"{self.name}-{mode}.json"

    def _saved(self, mode: str):
        if mode in self.mem:
            return self.mem[mode]
        try:
            data = json.loads(self._path(mode).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        self.mem[mode] = data
        return data

    def get(self, mode: str, force: bool = False) -> dict:
        """The data for a game mode. A new download when the saved data is too old or force is set.
        When the download fails, the old data is returned with "stale": true."""
        with self.lock:
            mode_lock = self.locks.setdefault(mode, threading.Lock())
        with mode_lock:   # two pages that ask at the same time cause one download
            old = self._saved(mode)
            if old and not force and time.time() - old.get("fetched", 0) < self.max_age:
                return old
            self.busy.add(mode)
            try:
                data = self.build(mode, self.fetch)
            except Exception as exc:
                self.errors[mode] = (time.time(), str(exc)[:200])
                if old:
                    return {**old, "stale": True}
                raise
            finally:
                self.busy.discard(mode)
            self.errors.pop(mode, None)
            self.mem[mode] = data
            try:
                self.folder.mkdir(parents=True, exist_ok=True)
                tmp = self._path(mode).with_suffix(".tmp")
                tmp.write_text(json.dumps(data), encoding="utf-8")
                tmp.replace(self._path(mode))
            except OSError:
                pass   # the data is still in memory
            return data

    def status(self, mode: str) -> dict:
        """What the Settings tab shows about the saved prices. No download is made here."""
        data = self._saved(mode)
        err = self.errors.get(mode)
        out = {"busy": mode in self.busy, "maxAge": self.max_age, "error": err[1] if err else None, "errorTime": err[0] if err else None}
        if data:
            out.update(fetched=data.get("fetched"), items=len(data.get("prices") or {}), crafts=len(data.get("crafts") or []))
            if "chapters" in data:   # the story chapters of story.py
                out.update(chapters=len(data["chapters"]), steps=sum(len(c.get("steps") or []) for c in data["chapters"]))
        return out
