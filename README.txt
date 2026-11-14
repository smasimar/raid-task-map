TARKOV QUEST MAP
================
A small local map that shows the quests you choose, your PMC extracts, and
your position from in-game screenshots. Progress is read from TarkovTracker.org.
TarkovMonitor stays in charge of updating TarkovTracker; this app only reads.

SETUP (once)
1. Install Python 3 from https://www.python.org/downloads/
   During setup, tick "Add python.exe to PATH".
2. Unzip this folder anywhere, for example Documents\TarkovQuestMap.
3. Double-click "Start Tarkov Quest Map.bat".
   A console window opens and your browser opens http://localhost:3000
   Keep the console window open while you play; close it to stop the app.
4. In the page, click Settings and paste a TarkovTracker.org API token.
   Create one on tarkovtracker.org > Settings > API Tokens. It needs read
   permission only, and it must be for the game mode you play: a PVP_ token
   shows PvP data, a PVE_ token shows PvE data.
5. In EFT, bind a key to "Screenshot" (Settings > Controls).

USING IT
- Pick the map you're on from the dropdown at the top. The screenshot file has
  no map name in it, so your marker is placed on the map you have selected.
- Press the screenshot key in a raid and your marker (blue arrow) moves there,
  pointing the way you were looking.
- Left panel: tick the tasks you actually have in-game. Only ticked tasks are
  drawn on the map. "Possible tasks on this map" lists tasks you might have,
  worked out from your TarkovTracker progress. It also contains tasks that
  trader dialogue hasn't unlocked yet (the API can't tell those apart), so tick
  only the ones in your in-game list. Use "Add a task by name" for anything
  missing.
- The "View" button changes between three views:
    Setup      the left panel, where you tick tasks.
    Mission <->  no panel; your quests show across the top of the map.
    Mission |    no panel; your quests show down the left side of the map.
  The mission list is semi-transparent. It shows your ticked quests for the
  selected map and the quests that have no fixed location. Completed steps are
  left out. Steps marked with a pin are on the map; click one to jump to it.
  Grey steps are on a different map.
- "My other quests" in the left panel lists ticked quests that are not on the
  selected map. The x removes a quest.
- A quest that is not in the tarkov.dev data yet (new quests) is added as text
  only when you add it by name. It has no steps or markers.
- Move the mouse over a quest marker to see its details.
- A ticked quest disappears by itself once TarkovTracker marks it complete.
  Progress reloads every 2 minutes; press "Progress" to reload it now.
- Map markers: yellow diamonds are objective zones, orange dots are possible
  quest-item spots, green boxes are PMC extracts, cyan boxes are shared extracts.
- "Floor" switches to upper floors or underground levels where the map has them.

FILES
- tarkov_quest_map.py  the local helper (Python standard library only)
- index.html           the map page
- maps.json            map projection settings, copied from tarkov.dev (MIT)
- config.json          created when you save Settings; it holds your token in
                       plain text, so don't share it

TROUBLESHOOTING
- "Port 3000 in use": set the TQM_PORT environment variable to another port,
  for example run:  set TQM_PORT=3005 && py tarkov_quest_map.py
- Marker doesn't move: check that Settings shows the screenshots folder as
  found. It's usually Documents\Escape From Tarkov\Screenshots.
- TarkovTracker answered 401: the token is wrong, revoked, or for another game mode.

Map images and game data come from tarkov.dev. Progress comes from tarkovtracker.org.
