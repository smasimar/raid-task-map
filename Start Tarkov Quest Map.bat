@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 tarkov_quest_map.py
  goto :eof
)
where python >nul 2>nul
if %errorlevel%==0 (
  python tarkov_quest_map.py
  goto :eof
)
echo Python 3 is not installed.
echo Get it from https://www.python.org/downloads/ and tick "Add python.exe to PATH" during setup.
pause
