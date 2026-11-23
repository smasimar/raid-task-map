"""Story chapters from TarkovTracker.org, with a link to the wiki for each step.

TarkovTracker lists the steps of each chapter with their game IDs. Its text is in a separate table
of strings. This module puts the two together, finds the wiki section of each step, and gives the
page a short list. crafts.CraftCache keeps the result in the cache folder for MAX_AGE seconds.

The wiki pages of the chapters have a guide with a heading for each stage. A step links to the
heading whose words are most like the step's words. A step with no close heading uses the heading
of another step of the same stage, or else the top of the chapter page.

Raid Task Map is free software under the GNU General Public License, version 3.
"""
import json
import re
import time
import urllib.parse
from pathlib import Path

from crafts import fetch_json

TRACKER = "https://tarkovtracker.org/api/tarkov"
WIKI_API = "https://escapefromtarkov.fandom.com/api.php"
MAX_AGE = 24 * 3600     # the chapters change only with a game patch
MATCH = 0.45            # the lowest score of a heading that a step links to
_STOP = set("the a an of to and or in on for from with any your you at by is be it that this i".split())


def _words(text: str) -> set:
    text = re.sub(r"<[^>]+>", "", text or "").lower()
    return {w for w in re.findall(r"[a-z0-9]+", text) if w not in _STOP}


def _score(step: set, head: set) -> float:
    """Half the shared part of all words, half the part of the step's words that the heading has."""
    same = len(step & head)
    return 0.0 if not same else 0.5 * same / len(step | head) + 0.5 * same / len(step)


def wiki_sections(page_url: str, fetch=fetch_json) -> list:
    """The headings of a wiki page below level 2: [(anchor, text)]. Empty when the wiki fails."""
    page = urllib.parse.unquote(page_url.rsplit("/wiki/", 1)[-1])
    url = f"{WIKI_API}?action=parse&prop=sections&format=json&redirects=1&page={urllib.parse.quote(page)}"
    try:
        secs = fetch(url).get("parse", {}).get("sections") or []
    except Exception:
        return []
    return [(s["anchor"], s["line"]) for s in secs
            if int(s.get("level") or 0) >= 3 and not re.match(r"(Rewards|Decision)\b", s.get("line", ""))]


def link_steps(steps: list, sections: list) -> dict:
    """step id -> wiki anchor, for the steps that have one."""
    heads = [(a, _words(t)) for a, t in sections]
    links = {}
    for s in steps:
        words = _words(s["text"])
        best = max(heads, key=lambda h: _score(words, h[1]), default=None)
        if best and _score(words, best[1]) >= MATCH:
            links[s["id"]] = best[0]
    stage = {}
    for s in steps:   # the first linked step of a stage gives its heading to the other steps
        if s["id"] in links:
            stage.setdefault(s.get("stage"), links[s["id"]])
    for s in steps:
        if s["id"] not in links and s.get("stage") in stage:
            links[s["id"]] = stage[s.get("stage")]
    return links


ROUTES_FILE = Path(__file__).resolve().parent / "story_routes.json"


def routes(path: Path = ROUTES_FILE):
    """The ending routes of The Ticket (story_routes.json), made ready for the page. None when the
    file is missing or broken. Each step gets "mark": the id that its done or failed mark uses,
    which is the TarkovTracker step id for a step with "ref"."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for sec in data["sections"].values():
            for st in sec["steps"]:
                if st.get("escape"):
                    st["text"] = data["escapeText"]
                if st.get("kind") != "note":
                    st["mark"] = st.get("ref") or st["id"]
        for r in data["routes"]:
            assert all(s in data["sections"] for s in r["sections"]), r["id"]
        return data
    except (OSError, ValueError, KeyError, AssertionError) as exc:
        print(f"[story] could not read {Path(path).name}: {exc}")
        return None


def build(mode: str, fetch=fetch_json) -> dict:
    """Download the chapters and their text for one game mode."""
    chapters = (fetch(f"{TRACKER}/editions?gameMode={urllib.parse.quote(mode)}").get("data") or {}).get("storyChapters") or []
    strings = (fetch(f"{TRACKER}/strings?lang=en&gameMode={urllib.parse.quote(mode)}").get("data") or {}).get("strings") or {}

    def text(v):
        return strings.get(v, "") if isinstance(v, str) and v.startswith("@tt:") else (v or "")

    def unlocks(items, kind=None):
        return [{"type": kind or u.get("type"), "id": u.get("id"), "name": text(u.get("name")), "note": text(u.get("note")) or None}
                for u in items or [] if text(u.get("name"))]

    out = []
    for c in sorted(chapters, key=lambda c: c.get("order") or 0):
        wiki = text(c.get("wikiLink"))
        steps = [{
            "id": o["id"], "text": text(o.get("description")), "optional": o.get("type") == "optional",
            "stage": o.get("sourceQuestId"), "parent": o.get("parentObjectiveId"), "ending": o.get("endingId"),
            "tutorial": o.get("completionPolicy") == "tutorial", "unlocks": unlocks(o.get("unlocks")),
        } for o in sorted((c.get("objectives") or {}).values(), key=lambda o: o.get("order") or 0)]
        links = link_steps(steps, wiki_sections(wiki, fetch)) if wiki else {}
        for s in steps:
            s["wiki"] = f"{wiki}#{links[s['id']]}" if s["id"] in links else wiki
        out.append({
            "id": c["id"], "name": text(c.get("name")) or c["id"], "order": c.get("order"), "questId": c.get("chapterQuestId"),
            "wiki": wiki, "autoStart": bool(c.get("autoStart")), "description": text(c.get("description")),
            "activation": text((c.get("activation") or {}).get("summary")), "notes": text(c.get("notes")),
            "rewards": text((c.get("rewards") or {}).get("description")),
            "requires": [{"id": r["id"], "name": text(r.get("name")) or r["id"]} for r in c.get("chapterRequirements") or []],
            "unlocks": unlocks(c.get("mapUnlocks"), "map") + unlocks(c.get("traderUnlocks"), "trader"),
            "exclusive": c.get("mutuallyExclusiveQuestPairs") or [],
            "endings": [{"id": e["id"], "name": e.get("systemName")} for e in c.get("endings") or []],
            "steps": steps,
        })
    return {"mode": mode, "fetched": time.time(), "chapters": out}
