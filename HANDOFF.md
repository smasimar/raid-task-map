# Tarkov Quest Map: handoff notes

This is a local replacement for the parts of Tarkov.dev's interactive map that the user actually uses. Read this before changing anything. It records what the user asked for, the decisions they made, and what was learned about the data sources while building it.

## What the user wants

- A map that shows **only the quests they have accepted in-game**, plus **PMC extracts**, plus **their own position** from in-game screenshots ("screenshot → map position").
- A **sidebar that lists the chosen quests with every step**, so they can see what they're going for at a glance.
- Nothing else from Tarkov.dev is needed.

### Constraints the user set (keep them)

1. **Don't parse the EFT logs.** The user runs **TarkovMonitor** alongside the game, and it keeps their progress up to date on **TarkovTracker.org**. All task tracking belongs to TarkovMonitor and TarkovTracker.
2. **This app never writes to TarkovTracker.** It only reads `GET /progress`.
3. **The user picks which quests are displayed**, by ticking them. Don't go back to "show everything computed as available" as the default. The show-all view is an opt-in radio option.
4. The user's API key is from **TarkovTracker.org**, not the legacy .io site. Tokens are prefixed `PVP_`, `PVE_` or `SZN_`.

## Why it was built: the original problem

The Tarkov.dev map and task list showed quests the user didn't have. Two causes:

- **Most likely, at the start:** Tarkov.dev historically read from **tarkovtracker.io**, while TarkovMonitor writes to **tarkovtracker.org**. The two sites use different keys and store data separately. The user says their .org key is now set up properly.
- **What remained:** neither site knows which quests have been *accepted*. They only know what's completed or failed, and they derive "available" from that.

## Key findings about the data sources (verified against source code and live data)

### TarkovTracker.org API: `https://api.tarkovtracker.org`
- Source repos: `tarkovtracker-org/TarkovTracker` (app, docs in `docs/api.md` and `docs/systems/progress-api.md`) and `tarkovtracker-org/TarkovTracker-API` (Cloudflare Worker).
- Endpoints: `GET /token`, `GET /progress`, `GET /team/progress`, plus write endpoints (unused): `POST /progress/level/{n}`, `/progress/task/{id}`, `/progress/task/objective/{id}`, `/progress/tasks`.
- **There is no endpoint that returns an active, accepted or available task list.** `TaskState` is only `completed | uncompleted | failed`.
- The `GET /progress` response is `{ data, meta }`. `data` contains:
  - `tasksProgress: [{id, complete, failed?, invalid?}]`. This only includes tasks the user has touched. `invalid` is computed only for those entries.
  - `taskObjectivesProgress: [{id, complete, count?, invalid?}]`
  - `tradersProgress: [{id, level, reputation}]`
  - `playerLevel`, `pmcFaction` (`USEC` or `BEAR`), `displayName`, `gameEdition`, plus hideout fields
- The game mode is decided by the token prefix (`PVP_` → pvp, `PVE_` → pve, `SZN_` → seasonal). Legacy `tt_` tokens get a 401.
- Required headers: `Authorization: Bearer <token>` and a `User-Agent` of 5–200 characters. It supports ETag / `If-None-Match`.
- **CORS** only allows `tarkovtracker.org`, `tarkov.dev` and `http://localhost:3000`. That's the reason for the local Python proxy: a hosted page can't call the API.
- **Quota:** the free tier allows 1,000 reads per day per account, and a 304 still counts. The page polls every 2 minutes while visible.
- TarkovTracker's own "available" calculation (`app/stores/taskAvailability.ts`, `taskServerGates.ts`) also uses data the API doesn't expose: manual "mark available" confirmations (`taskAvailability`), global variables, story chapters and overlay counters. **So no client of the API can fully reproduce TarkovTracker's list.**

### tarkov.dev game data: `https://json.tarkov.dev` (CORS `*`)
- Endpoints: `/{regular|pve|pvp-season}/{tasks,maps,traders,...}`, plus `_<lang>` translation files such as `/regular/tasks_en`. `/endpoints` lists them all.
- In the main files, strings are **translation keys**. The task name key looks like `"<taskId> name"`. An objective's `description` key is the objective id. Map names look like `"<mapId> Name"`. Extract names look like `ex_customs_...`. The app translates specific fields only. Don't walk the whole object, because objective `id === description` key.
- References are plain id strings: `task.trader`, `taskRequirements[].task`, `zones[].map`, `possibleLocations[].map`.
- Task fields used: `minPlayerLevel`, `factionName`, `taskRequirements[{task, status[]}]` (status values: `complete`, `active`, `failed`), `traderRequirements[{trader, requirementType: level|reputation, compareMethod, value}]`, `failConditions`, `finishRewards.traderUnlock`, `objectives[{id, description, type, count, optional, maps[], zones[{map, position, outline, top, bottom}], possibleLocations[{map, positions[]}]}]`, `otherRequirements[{type: dialogue|globalVariable}]`, `wikiLink`.
- About 180 of 503 tasks have `otherRequirements` (dialogue gates). Even "First in Line" has one. Applying these gates would hide starter quests, and the API can't tell whether they're satisfied, so the app ignores them. As a result, the "possible tasks" list over-includes, which is why the user ticks their quests by hand.
- Map extract `faction` values are `pmc`, `scav`, `shared` and `null`. The app treats `null` as shared and hides `scav`.
- The old GraphQL API at `api.tarkov.dev` is described as deprecated in TarkovTracker's docs. Don't use it.

### Map rendering (ported from `the-hideout/tarkov-dev` `src/pages/map/index.jsx`)
- `maps.json` is the interactive entries from tarkov-dev `src/data/maps.json` (MIT). It holds `transform`, `coordinateRotation`, `bounds`, `svgPath`/`svgLayer`, `tilePath`, `layers` (floors) and `labels`.
- The CRS is `L.CRS.Simple` with `L.Transformation(t0, t1, -t2, t3)` and a custom projection that rotates by `coordinateRotation`. The position mapping is `[z, x]`. I checked this visually on Customs: extracts land correctly.
- SVG maps: fetch the SVG, keep the top-level `<g id>` that matches `svgLayer` as the base, and hide the others. Floors either show another group with the base dimmed, or add a floor tile layer.
- The player arrow's rotation is the yaw plus `coordinateRotation`, with an extra +180° when that is 90 or 270, the same as tarkov.dev.

### Screenshot → position (ported from `the-hideout/TarkovMonitor` `GameWatcher.cs`)
- The screenshots folder is `Documents\Escape From Tarkov\Screenshots`. The app resolves the real Documents folder via `SHGetFolderPathW`, which handles OneDrive redirection.
- Filename pattern: `YYYY-MM-DD[HH-MM]_x, y, z_qx, qy, qz, qw_... (N).png`. The regexes are copied from TarkovMonitor.
- Yaw uses TarkovMonitor's `QuarternionsToYaw(x, z, y, w)`, including its swapped parameter names, so it matches tarkov.dev's arrow.
- **The filename has no map name.** Since log parsing is ruled out, the position is placed on the map the user has selected.

## Architecture

```
tarkov_quest_map.py   Python 3 stdlib only. ThreadingHTTPServer on 127.0.0.1:3000 (env TQM_PORT)
  GET  /                -> index.html
  GET  /maps.json       -> vendored map config
  GET  /api/config      -> public config (hasToken, tokenHint, gameMode from token prefix, folders)
  POST /api/config      -> save token / screenshotsDir / deleteScreenshots to config.json
  GET  /api/progress    -> proxies api.tarkovtracker.org/progress (ETag cache, stale fallback)
  GET  /api/state       -> last position event
  GET  /api/events      -> Server-Sent Events stream of {type:"position", x,y,z, rotation, filename}
  POST /api/test-position -> inject a fake position (debugging without the game)
  Thread: polls the screenshots folder every 0.5 s and ignores files already present at start

index.html            Single page, Leaflet 1.9.4 from unpkg; fetches game data directly from json.tarkov.dev
  Left panel:   profile, layer toggles, show mode (ticked only / every possible task), add-task-by-name,
                ticked tasks on this map, collapsed "Possible tasks on this map"
  Map:          base (svg/tile), floors, labels, PMC+shared extracts, quest markers, player arrow
  Right panel:  "My quests": every ticked quest, all steps with counts; current-map group first;
                📍 steps clickable to fly to the marker. Toggle with "☰ Quest list".
  localStorage: tqm.selected.<mode> (ticked task ids), tqm.map, tqm.style, tqm.showMode, tqm.questPanel
```

The task logic in `computeAvailable()` approximates TarkovTracker's rules: not done, failed or invalid; player level; faction; trader level and reputation; a failCondition completed on an alternative branch; prerequisite statuses (an `active` prerequisite counts if that task is itself available); and trader unlocks (`finishRewards.traderUnlock`, plus hardcoded Lightkeeper, BTR driver and Ref unlock tasks from TarkovTracker's `constants.ts`). It only feeds the "possible tasks" suggestions. What's drawn is decided by the user's ticks. Ticks are removed automatically once TarkovTracker reports the task complete or failed.

## Files

| File | Purpose |
|---|---|
| `tarkov_quest_map.py` | Local helper/server |
| `index.html` | The whole UI |
| `maps.json` | Map projection settings (from tarkov.dev, MIT) |
| `Start Tarkov Quest Map.bat` | Windows launcher (tries `py -3`, then `python`) |
| `README.txt` | User-facing setup guide |
| `tests/e2e.test.js` | Headless jsdom + Leaflet run of `index.html` with fixtures shaped like the real data (23 checks) |
| `config.json` | Created at runtime; holds the token in plain text |

Run the tests with: `cd tests && npm install && npm test`

## Testing status

- **Tested:** the Python server (config save, missing-token error, screenshot detection → SSE event, yaw math); the page end-to-end in jsdom (gating rules, ticking, add-by-name, quest panel grouping and steps, markers, extract filtering, map switching, player marker, auto-removal on completion); and real projection plus extract placement on Customs, checked visually in a browser against live json.tarkov.dev data.
- **Not yet tested:**
  - Against the user's real TarkovTracker account. The development sandbox couldn't reach `api.tarkovtracker.org`.
  - On Windows itself: the launcher, the Documents path lookup, and opening the browser.
  - Tile-based maps (Labs, Labyrinth, Icebreaker) and floor switching in a real browser.

## Known limitations and ideas

- The "possible tasks" list over-includes, because dialogue gates aren't visible through the API. That's by design; the user ticks quests manually.
- The map must be selected by hand for screenshots. If the user ever relaxes the no-log-parsing rule, TarkovMonitor's `Location: <nameId>` log line maps to the API map's `nameId`.
- Objectives without positions (kill X anywhere, hand over items) appear only as text steps.
- Possible next steps: filter the quest panel per trader; a hotkey to toggle panels; a "rotate the map to the player's facing" option; supporting `If-None-Match` from the page to save bandwidth (it still counts against the quota).

## Review pass (2026-11-14, Claude Code)

Fixed after a code review:

- **Server:** rejects requests whose `Host`/`Origin` is not local, and POSTs that are not `application/json` (CSRF, DNS rebinding). `/api/progress` reuses its cache for 60 s (5 s with `?force=1`, used by the "↻ Progress" button), so several tabs share one upstream read. Cached progress is served with `X-Stale: 1` on network errors, 429 and 5xx. A 304 with an empty cache is retried without the ETag. `config.json` is written atomically. The screenshot pattern accepts `(12)` and exponent-form quaternion parts.
- **Page:** ticked quests are drawn without progress data. `showMap` and `showFloor` ignore results from a superseded call. Zone outlines are always drawn. Markers on other floors are dimmed (`floorOf()` uses `layers[].extents` from `maps.json`), and the floor follows the screenshot height. An unchanged progress answer does not re-render (open popups stay). A stale answer shows in the status line. A saved position older than 10 minutes is ignored at start. Leaflet tags have SRI hashes. Dead code removed.
- **Tests:** `tests/test_server.py` (`py -3 -m unittest discover tests`) covers the filename parser, the request check and the token-prefix mode. `e2e.test.js` now checks the markers in show-all mode.

Verified in a real browser against live json.tarkov.dev data, without a token: quest markers without progress, fast map change, floor follow on Customs, 415/403/400 answers. **Not run:** `tests/e2e.test.js` (no Node on this PC), and anything against a real TarkovTracker account.

## UI changes after the review (2026-11-14)

- **The right-hand "My quests" panel is gone.** One header button (`#viewBtn`, `setView()`, stored in `tqm.view`) cycles three views: `setup` (left panel), `mission-h` and `mission-v`. The mission views hide the left panel and show `#mission` over the map: semi-transparent cards for the ticked quests on the selected map, then "any location" quests, then text-only quests. Completed steps are left out. Only the cards take mouse input, so the map can be dragged between them.
- **"My other quests"** (`#elseBox`) in the left panel lists ticked quests that are not on the selected map, with a remove button.
- **Text-only quests:** a name that tarkov.dev does not have (for example "A Familiar Face...", checked 2026-11-14 in all three game modes) is stored in `tqm.custom.<mode>` and shown without steps or markers.
- **Quest markers** show a tooltip on hover (`bindTooltip`), not a popup on click. The zoom buttons are at the bottom right.
- The user asked for a local git repository only. Do not add a remote or push.
