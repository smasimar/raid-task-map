# Raid Task Map

A small local companion for Escape from Tarkov. It shows the quests you select, the
extracts, and your position on an interactive map, and it follows your raids through
the game's log files.

It runs on your PC as a local web page. It reads only log files and screenshots. It
does not read the game's memory, network traffic or game files.

> **Status:** work in progress. Some files still carry the working name
> "Tarkov Quest Map". See [Roadmap](#roadmap).

## Features

- **Quest map.** Objective zones, quest-item locations and extracts for the quests you
  tick, with floors for maps that have more than one level.
- **Your position.** Press the screenshot key in a raid; a marker shows where you are
  and where you look.
- **Raid tracking.** When a raid loads, the app selects the map, shows your mission
  list and starts a raid timer. After the raid it goes back to the setup panel.
- **Automatic quest list.** A quest that you accept in the game is ticked by itself,
  and it is removed when you complete or fail it. "Read past logs" finds the quests
  you accepted before the app ran.
- **Three views.** A setup panel to select quests, and two mission views that put a
  semi-transparent quest list over the map (across the top, or down the side).
- **Progress from TarkovTracker.** Completed quests and steps disappear from the list.
- **Progress to TarkovTracker (optional).** Quests that you complete or fail in the
  game are sent to TarkovTracker. You can mark steps and counts by hand on the mission
  cards. Fast clicks on one step are sent as one change, and changes that cannot be
  sent are kept and sent later.
- **PvP and PvE.** Each game mode has its own token and its own quest list. The app
  follows the mode that the game runs in.

## Requirements

- Windows 10 or 11
- [Python 3.9 or later](https://www.python.org/downloads/) (tick "Add python.exe to
  PATH" during setup). No other packages are necessary.
- A [TarkovTracker.org](https://tarkovtracker.org) account, for quest progress

## Setup

1. Download or clone this repository.
2. Double-click `Start Tarkov Quest Map.bat`. A console window opens, and your browser
   opens <http://localhost:3000>. Keep the console window open while you play.
3. Click **Settings** and paste a TarkovTracker API token. Create one on
   tarkovtracker.org → Settings → API Tokens. The token decides the game mode: a
   `PVP_` token is for PvP progress, a `PVE_` token is for PvE progress. To use two
   modes, paste one token for each.
4. Optional: tick **Send quest progress to TarkovTracker**. The token then needs the
   "Write progress" permission. With this on, you do not need TarkovMonitor for quest
   tracking.
5. In the game, bind a key to **Screenshot** (Settings → Controls).

The app finds the game's `Logs` folder and your screenshots folder automatically. If
it does not, type the paths in **Settings**.

## Use

| Action | Result |
| --- | --- |
| Tick a quest in the setup panel | The quest shows on the map and in the mission list |
| **Read past logs** | Reads the game's old log files and proposes the quests to tick. It changes only the list in this app |
| "Add a task by name" | Adds a quest that is not in the list. A quest that tarkov.dev does not know yet is added as text only |
| **View** button | Changes between Setup, Mission ↔ (list across the top) and Mission ↕ (list down the side) |
| Click a 📍 step in the mission list | The map moves to that objective |
| **−** / **+** / **✓** on a step | Changes the count of the step, or marks it done. Shown when sending to TarkovTracker is on |
| **✓ quest** on a mission card | Marks the quest as completed on TarkovTracker |
| **↺** on a done step in the setup panel | Marks the step as not done |
| Mouse over a marker | Shows the quest and the step |
| Screenshot key in a raid | Moves your position marker |
| **⌖ Reset view** | Puts the full map back in the window |
| **↻ Progress** | Reads your progress from TarkovTracker now (otherwise every 2 minutes) |

Map markers: yellow diamonds are objective zones, orange dots are possible quest-item
locations, green boxes are PMC extracts, cyan boxes are shared extracts.

The screenshot file has no map name in it. Your marker goes on the selected map, which
is the raid's map when raid tracking is on.

## Troubleshooting

- **"Port 3000 in use".** Start the app on a different port:
  `py tarkov_quest_map.py --port 3005`
- **The marker does not move.** Make sure that Settings shows the screenshots folder as
  found. It is usually `Documents\Escape From Tarkov\Screenshots`.
- **The map does not change when a raid loads.** Make sure that Settings shows the logs
  folder as found, and that "Select the map when a raid loads" is ticked.
- **"Read past logs" proposes quests that you completed.** The game deletes old logs,
  so some completions are missing. Quests that TarkovTracker shows as completed are
  left out; untick the others.
- **"TarkovTracker daily write limit reached".** A free account can send 100 changes
  each day. The app keeps your changes and sends them after the limit resets at
  00:00 UTC.
- **TarkovTracker answered 401.** The token is wrong, revoked, or for a different game
  mode.

## Privacy

- The app listens only on `127.0.0.1` and refuses requests from other sites.
- Your tokens are stored in `config.json` next to the app, in plain text. Do not share
  that file. It is excluded from git.
- The app contacts only `tarkov.dev` (maps and game data), `unpkg.com` (the Leaflet
  map library) and `api.tarkovtracker.org` (your progress).

## Development

```
py -3 tarkov_quest_map.py --no-browser      start without opening the browser
py -3 -m unittest discover tests            server and log-reader tests
cd tests && npm install && npm test         page tests (Node.js and jsdom)
```

| File | Purpose |
| --- | --- |
| `tarkov_quest_map.py` | Local server: static page, TarkovTracker proxy, screenshot and log watchers, live events |
| `game_logs.py` | Game log reader and raid state |
| `index.html` | The full page: map, quest lists, settings |
| `maps.json` | Map projection settings, from tarkov.dev |
| `state.json` | Your quest list for each game mode, and the changes that wait to be sent. Made by the app; excluded from git |
| `tests/fixtures` | Lines from a real game session, with IDs and addresses masked |

## Roadmap

The aim is to do the work of TarkovMonitor for this app's features, so that one app
is sufficient.

- [x] Read the game logs: map selection, mission view, raid timer, game mode
- [x] Tick quests automatically when you accept them in the game
- [x] Send completed and failed quests to TarkovTracker; mark steps done by hand
- [ ] New name in all files, release package

## Credits and licenses

- **This app:** [GPL-3.0](LICENSE).
- **Log patterns and raid state logic** are ported from
  [TarkovMonitor](https://github.com/the-hideout/TarkovMonitor) (GPL-3.0).
- **Maps:** [tarkov.dev](https://tarkov.dev) and their authors, mainly Shebuka,
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). The maps are
  loaded from tarkov.dev when the app runs; none are included here. Their license
  forbids commercial use and use in cheat software.
- **Game data:** the [tarkov.dev](https://tarkov.dev) API. `maps.json` is from the
  tarkov-dev project (MIT).
- **Quest progress:** [TarkovTracker.org](https://tarkovtracker.org).
- **Map library:** [Leaflet](https://leafletjs.com) (BSD 2-Clause).

This project is not affiliated with or approved by Battlestate Games. Escape from
Tarkov is a trademark of Battlestate Games Limited. The game's license agreement does
not give permission for tools that read its files; use this app at your own risk.
