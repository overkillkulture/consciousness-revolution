@echo off
echo Starting Cyclotron Daemon...
echo.
echo Services:
echo - Port 6668: Filename search (CYCLOTRON_SEARCH.py)
echo - Port 6669: Content search (CYCLOTRON_SEARCH_V2.py)
echo - Daemon: File watcher with auto-indexing
echo.
cd /d C:\Users\dwrek\100X_DEPLOYMENT

echo Starting filename search API (port 6668)...
start /B python CYCLOTRON_SEARCH.py

echo Starting content search API (port 6669)...
start /B python CYCLOTRON_SEARCH_V2.py

echo Starting daemon (file watcher)...
python CYCLOTRON_DAEMON.py

echo.
echo Cyclotron fully operational!
