# Raid Task Map

A local companion for Escape from Tarkov. It shows your tasks, their locations, the
extracts and your position on a map.

It reads only the game's log files and the file names of your screenshots (the game
writes your position into them). It does not read game memory or network traffic, and
it does not change game files. The game's license agreement does not permit such tools.
Use the app at your own risk.

## Features

- **Tasks tab:** tick the tasks you have. "My tasks" lists them. Each trader shows its
  task lines and the state of each task: completed, in progress, available or locked.
- **Map tab:** objective zones, task-item locations, extracts and floors for the selected
  map. The mission list shows your ticked tasks for that map.
- **Position:** press the screenshot key in a raid. A blue arrow shows where you are and
  which way you look.
- **Game logs:** a task you accept is ticked; a task you complete or fail is unticked.
  When a raid loads, the app selects the map and the PMC or Scav extracts and starts a
  raid timer. After the raid it goes back to the Tasks tab. Settings can turn off the
  map selection and the tab change.
- **TarkovTracker:** the app reads your progress from
  [TarkovTracker.org](https://tarkovtracker.org), so completed tasks and steps drop off
  your lists. If you allow it, it also sends task
  changes, step counts and your level.
- **Status tab:** the state of TarkovTracker, game data, logs and screenshots, the
  changes that wait to be sent, and a list of what the app did.
- PvP and PvE have separate task lists.

## Requirements

- Windows 10 or 11
- [Python 3.9 or later](https://www.python.org/downloads/). Tick "Add python.exe to
  PATH" during setup. No other packages are necessary.
- Optional: a TarkovTracker account. Without one, the app does not know what you have
  completed.

## Setup

1. Download or clone this repository.
2. In that folder, run `py raid_task_map.py`. The browser opens
   <http://localhost:3000>. Keep the terminal open while you play. Ctrl+C stops the app.
3. On tarkovtracker.org → Settings → API Tokens, create a token that can read progress.
   Paste it on the app's **Settings** tab and click **Save**.
4. Optional: tick **Send task progress to TarkovTracker** and click **Save**. The token
   then also needs "Write progress".
5. In the game (Settings → Controls), bind a key to **Screenshot**.
6. On the Tasks tab, tick your tasks, or click **Read past logs**.

A token is for one game mode (`PVP_` or `PVE_` prefix). To use both modes, save one
token, then save the other in the same box. While the game runs, the app uses the
game's mode; otherwise it uses **Game mode** on the Settings tab.

The app finds the `Logs` and screenshots folders automatically. If Settings shows one
as not found, type its path.

## Use

- **Tasks tab.** Click a task name to see its steps. Use search, filters and **Sort**.
  ↗ opens the wiki page.
- **Map tab.** Click a step marked 📍 to move the map to it. **List ↔ / ↕ / ✕** puts
  the mission list across the top, down the side, or hides it. **Mini** (key **M**)
  shows only the map, extracts and task locations. **M** or **Esc** goes back. **Layers** sets PMC or Scav extracts and shows or
  hides objectives, extract names and landmark names.
- **Progress** (with sending on). Type a step count, mark a step or task done with
  **✓**, undo with **↺**. Type your level in the box next to your name; the game logs
  do not give it.

Map markers:

| Marker | Meaning |
| --- | --- |
| Yellow diamond | Objective zone |
| Orange dot | Possible task-item location |
| Green box | PMC extract |
| Orange box | Scav extract |
| Cyan box | PMC and Scav extract |
| Pale box | Extract with a requirement (payment, key, no backpack, Red Rebel and paracord, partner). Point at it to see what it needs |
| 🔑 | Key that a task or step needs |

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `py` is not recognized | Install Python (see Requirements). |
| "Could not start on port 3000" | Run `py raid_task_map.py --port 3005`. |
| The marker does not move | Check that Settings finds the screenshots folder (usually `Documents\Escape From Tarkov\Screenshots`) and that the Map tab shows your map. |
| The map does not change when a raid loads | Check that Settings finds the logs folder and that "Select the map when a raid loads" is ticked. |
| "Read past logs" proposes completed tasks | The game deletes old logs. Tasks that TarkovTracker shows as completed are left out; untick the others. |
| "TarkovTracker daily write limit reached" | A free account can send 100 changes a day. The app sends the rest after 00:00 UTC. |
| "TarkovTracker answered 401" | The token is wrong, revoked or for the other game mode. |

## Privacy

- The app listens only on `127.0.0.1` and refuses requests from other sites.
- Tokens are in `config.json` in plain text. Do not share it. Git ignores it.
- Ticked tasks and unsent changes are in `state.json`.
- The app contacts only `tarkov.dev`, `unpkg.com` (Leaflet) and `api.tarkovtracker.org`.
- Screenshots are deleted only if you tick that option in Settings (off by default).

## Development

```
py -3 raid_task_map.py --no-browser      start without opening the browser
py -3 -m unittest discover tests         server and log-reader tests
cd tests; npm install; npm test          page tests (Node.js and jsdom)
```

| File | Purpose |
| --- | --- |
| `raid_task_map.py` | Local server: page, TarkovTracker proxy, screenshot and log watchers |
| `game_logs.py` | Game log reader and raid state |
| `index.html` | The page: map, task lists, settings |
| `maps.json` | Map projection settings, from tarkov.dev |
| `config.json`, `state.json` | Your settings and task lists. Made by the app; git ignores them |
| `tests/fixtures` | Log lines from a real game session, IDs and addresses masked |

## Credits and licenses

- License: [GPL-3.0](LICENSE).
- Log patterns and raid state logic are ported from
  [TarkovMonitor](https://github.com/the-hideout/TarkovMonitor) (GPL-3.0).
- Maps: [tarkov.dev](https://tarkov.dev) and their authors, mainly Shebuka, under
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). They are loaded
  at run time; none are in this repository. Their license forbids commercial use and
  use in cheat software.
- Game data: the [tarkov.dev](https://tarkov.dev) API. `maps.json` is from the
  tarkov-dev project (MIT).
- Task progress: [TarkovTracker.org](https://tarkovtracker.org).
- Map library: [Leaflet](https://leafletjs.com) (BSD 2-Clause), loaded from unpkg.com.

This project is not affiliated with or approved by Battlestate Games. Escape from
Tarkov is a trademark of Battlestate Games Limited.
