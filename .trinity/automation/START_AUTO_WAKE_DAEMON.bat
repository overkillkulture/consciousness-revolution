@echo off
REM START_AUTO_WAKE_DAEMON.bat
REM Launch the Auto Wake Daemon for cross-computer coordination

echo ========================================
echo STARTING AUTO WAKE DAEMON
echo ========================================
echo.

cd /d C:\Users\darri\100X_DEPLOYMENT

echo Computer: %COMPUTERNAME%
echo Working Directory: %CD%
echo.

echo Starting AUTO_WAKE_DAEMON.py...
echo.
echo Daemon will monitor .trinity\wake\ for wake signals
echo Check interval: 30 seconds
echo Logs: .trinity\logs\auto_wake_daemon.log
echo.
echo Press Ctrl+C to stop the daemon
echo ========================================
echo.

python .trinity\automation\AUTO_WAKE_DAEMON.py
