@echo off
REM START ENTIRE TRINITY SYSTEM
REM Run this to launch all coordination components

echo.
echo  ========================================
echo   TRINITY COORDINATION SYSTEM STARTUP
echo  ========================================
echo.

REM Set computer ID
set COMPUTER_ID=PC1

REM Pull latest from git
echo [1/4] Syncing with git...
cd %USERPROFILE%\100X_DEPLOYMENT
git pull

REM Start the daemon in background
echo [2/4] Starting coordination daemon...
start "Trinity Daemon" cmd /k "set COMPUTER_ID=%COMPUTER_ID% && python .trinity\automation\CROSS_COMPUTER_DAEMON.py"

REM Check for pending tasks
echo [3/4] Checking for pending tasks...
python -c "from pathlib import Path; import json; p=Path.home()/'100X_DEPLOYMENT'/'.trinity'/'tasks'/'pending'; tasks=[f.name for f in p.glob('*.json')] if p.exists() else []; print(f'Pending tasks: {len(tasks)}')"

REM Open Claude Code if tasks pending
echo [4/4] Ready for work...
echo.
echo ========================================
echo  SYSTEM STARTED
echo ========================================
echo.
echo Daemon running in background window
echo Git synced and watching for changes
echo.
echo TO START WORKING:
echo   1. Open new terminal
echo   2. Run: claude
echo   3. Say: "Check pending tasks and execute"
echo.
echo TO WAKE OTHER COMPUTERS:
echo   python -c "from CROSS_COMPUTER_DAEMON import CoordinationDaemon; d=CoordinationDaemon(); d.send_wake_signal('PC2', 'Need help with task', 'open_claude')"
echo.
pause
