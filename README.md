# Raid Task Map

A small local companion for Escape from Tarkov. You tick the tasks you have in the
game, and the app shows where their steps are, the extracts and your position on an
interactive map. It reads the game's log files to select the raid's map, time the raid
and tick the tasks you accept.

It runs on your PC as a local web page. It reads two things: the game's log files, and
the names of your screenshots (the game writes your position into the file name of
each screenshot). It does not read the game's memory or network traffic, and it does
not change any game file.

The game's license agreement does not give permission for tools that read its log
files or screenshots. Use this app at your own risk.

Task progress is kept on [TarkovTracker.org](https://tarkovtracker.org), a free
website that tracks which tasks and task steps you have completed. The app reads your
progress from there and, if you allow it, sends your progress there. The list of tasks
you ticked is kept by the app, on your PC.

## Features

The page has four tabs: Tasks, Map, Status and Settings.

- The Tasks tab is where you tick tasks. Its left column has "My tasks" and one entry
  for each trader; the tasks of the selected entry show on the right, each with a tick
  box. "My tasks" lists the tasks you have ticked. A trader's entry shows the trader's
  task lines (chains of tasks, where each task opens the next) and the state of each
  task: completed, in progress, available or locked.
- The Map tab shows one map at a time, which you select in the top bar. It shows
  objective zones, the locations of items that a task needs, and extracts for your
  ticked tasks, with a floor selector for maps that have more than one level. Your
  ticked tasks for the selected map are listed over the map, semi-transparent, across
  the top or down the side. This list is called the mission list.
- Press your screenshot key in a raid and a marker shows where you are and which way
  you are looking.
- A task that you accept in the game is ticked automatically, and it is unticked when
  you complete or fail it. "Read past logs" on the Tasks tab finds the tasks you
  accepted before the app was running, shows them, and ticks them if you agree.
- When a raid loads, the app selects the raid's map and opens the Map tab, and after
  the raid it goes back to the Tasks tab. You can turn off the map selection and the
  tab change in Settings. A timer in the top bar shows the time in the raid and the
  time left.
- The app shows Scav extracts in a Scav raid and PMC extracts otherwise.
- The app reads your progress from TarkovTracker, so completed tasks drop off "My
  tasks" and the mission list, and completed steps drop off the mission list.
- Optionally, the app also sends progress to TarkovTracker: the tasks you complete or
  fail in the game, and the steps and counts (for example 7 of 10 kills) that you mark
  by hand on the Tasks tab.
- The Status tab shows whether TarkovTracker, the game data, the game logs and the
  screenshots folder are working, how many log lines the app has read, how many
  changes wait to be sent, and a list of what the app did.
- PvP and PvE each have their own task list.

## Requirements

- Windows 10 or 11
- [Python 3.9 or later](https://www.python.org/downloads/) (tick "Add python.exe to
  PATH" during setup). The app uses only what comes with Python.
- A [TarkovTracker.org](https://tarkovtracker.org) account. Without one, the map and
  the task list still work, but the app does not know what you have completed.

## Setup

1. Download or clone this repository.
2. Open a terminal in that folder and run `py raid_task_map.py`. Your browser opens
   <http://localhost:3000>. Keep the terminal open while you play; press Ctrl+C or
   close it to stop the app.
3. Create an API token on tarkovtracker.org → Settings → API Tokens, with permission
   to read your progress. A token is a key that lets the app use your TarkovTracker
   account. Open the app's **Settings** tab, paste the token and click **Save**. You
   can skip this step if you have no account.
4. Optional: tick **Send task progress to TarkovTracker** and click **Save**. The
   token then needs the "Write progress" permission too. With this on, you do not need
   TarkovMonitor (the tarkov.dev app that updates TarkovTracker from the game logs),
   so you can close it.
5. In the game's own settings (Settings → Controls), bind a key to **Screenshot**.
6. On the Tasks tab, tick the tasks you have in the game, or click **Read past logs**
   to let the app propose them.

TarkovTracker makes each token for one game mode, and the token's prefix shows which:
`PVP_` or `PVE_`. To use both modes, paste and save one token, then paste and save the
other in the same box; the app keeps both. While the game is running, the app shows
the mode the game is in. When the game is not running, the **Game mode** selector on
the Settings tab selects the mode.

The app finds the game's `Logs` folder and your screenshots folder automatically. The
Settings tab shows each folder as found or not found; if one is not found, type its
path there.

## Use

- **Tasks tab.** Tick the tasks you have in the game. Click a task name to see its
  steps. The search box, the filters and **Sort** narrow and order the list.
- **Map tab.** Select a map in the top bar. Click a step marked 📍 in the mission list
  to move the map to it. The **List ↔** / **List ↕** button moves the mission list.
- **In a raid.** Press your screenshot key to move your position marker (a blue
  arrow). The marker goes on the selected map.
- **Progress.** With "Send task progress to TarkovTracker" on, the Tasks tab lets you
  type the count of a step (for example 7 of 10 kills), mark a step or a task as done
  with **✓**, and undo that with **↺**.

Map markers: yellow diamonds are objective zones, orange dots are possible task-item
locations, green boxes are PMC extracts, orange boxes are Scav extracts, and cyan boxes
are extracts that both PMCs and Scavs can use.

The app works out from the game logs whether a raid is a PMC raid or a Scav raid, and
shows the extracts for that side. If it gets this wrong, select PMC or Scav in the
**Extracts** setting on the Settings tab.

## Troubleshooting

- **`py` is not recognized.** Python is not installed. Install it from the link in
  Requirements.
- **The terminal says "Could not start on port 3000".** Start the app on a different
  port: `py raid_task_map.py --port 3005`
- **The marker does not move.** Check that Settings shows the screenshots folder as
  found. It is usually `Documents\Escape From Tarkov\Screenshots`. Check also that the
  Map tab shows the map you are on, because the marker goes on the selected map.
- **The map does not change when a raid loads.** Check that Settings shows the logs
  folder as found, and that "Select the map when a raid loads" is ticked.
- **"Read past logs" proposes tasks that you completed.** The game deletes old logs,
  so some completions are missing from them. The app leaves out the tasks that
  TarkovTracker shows as completed. Untick any other completed task yourself.
- **The top bar says "TarkovTracker daily write limit reached".** A free account can
  send 100 changes each day. The app keeps your changes and sends them after the limit
  resets at 00:00 UTC.
- **The top bar says "TarkovTracker answered 401".** The token is wrong, revoked, or
  for a different game mode.

## Privacy

- The app listens only on `127.0.0.1` and refuses requests from other sites.
- Your tokens are stored in `config.json` next to the app, in plain text. Do not share
  that file. It is excluded from git.
- Your ticked tasks are stored in `state.json` next to the app.
- The app contacts only `tarkov.dev` (maps and game data), `unpkg.com` (the Leaflet
  map library) and `api.tarkovtracker.org` (your progress).
- The app deletes a screenshot only if you tick "Delete each screenshot after reading
  its position" in Settings. This is off by default.

## Development

```
py -3 raid_task_map.py --no-browser      start without opening the browser
py -3 -m unittest discover tests            server and log-reader tests
cd tests; npm install; npm test             page tests (Node.js and jsdom)
```

| File | Purpose |
| --- | --- |
| `raid_task_map.py` | Local server: static page, TarkovTracker proxy, screenshot and log watchers. It sends your position, the raid state and list changes to the open page |
| `game_logs.py` | Game log reader and raid state |
| `index.html` | The full page: map, task lists, settings |
| `maps.json` | Map projection settings, from tarkov.dev |
| `config.json` | Your settings and tokens. Made by the app; excluded from git |
| `state.json` | Your task list for each game mode, and the changes waiting to be sent. Made by the app; excluded from git |
| `tests/fixtures` | Log lines from a real game session, with IDs and addresses masked |

## Credits and licenses

- This app is licensed under [GPL-3.0](LICENSE).
- The log patterns and the raid state logic are ported from
  [TarkovMonitor](https://github.com/the-hideout/TarkovMonitor) (GPL-3.0).
- The maps are from [tarkov.dev](https://tarkov.dev) and their authors, mainly
  Shebuka, under
  [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). They are
  loaded from tarkov.dev when the app runs; none are included in this repository.
  Their license forbids commercial use and use in cheat software.
- The game data comes from the [tarkov.dev](https://tarkov.dev) API. `maps.json` is
  from the tarkov-dev project (MIT).
- Task progress comes from [TarkovTracker.org](https://tarkovtracker.org).
- The map library is [Leaflet](https://leafletjs.com) (BSD 2-Clause), loaded from
  unpkg.com.

This project is not affiliated with or approved by Battlestate Games. Escape from
Tarkov is a trademark of Battlestate Games Limited.
