@echo off
REM SETUP WEEKLY CREDIT BURNER SCHEDULE
REM Run this once to schedule weekly credit burns

echo === SETTING UP WEEKLY CREDIT BURNER ===
echo.

REM Set computer ID (change for each computer)
set COMPUTER_ID=PC1

REM Create scheduled task for Sunday at 8 PM
schtasks /create /tn "Trinity Weekly Credit Burn" /tr "python %USERPROFILE%\100X_DEPLOYMENT\.trinity\automation\WEEKLY_CREDIT_BURNER.py" /sc weekly /d SUN /st 20:00 /f

if %errorlevel% equ 0 (
    echo SUCCESS: Weekly credit burn scheduled for Sunday 8 PM
) else (
    echo ERROR: Failed to create scheduled task
    echo Try running as Administrator
)

echo.
echo === SETUP DAEMON AUTO-START ===

REM Create startup shortcut for daemon
set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
echo Creating startup shortcut...

echo @echo off > "%STARTUP%\TrinityDaemon.bat"
echo cd %USERPROFILE%\100X_DEPLOYMENT >> "%STARTUP%\TrinityDaemon.bat"
echo set COMPUTER_ID=%COMPUTER_ID% >> "%STARTUP%\TrinityDaemon.bat"
echo python .trinity\automation\CROSS_COMPUTER_DAEMON.py >> "%STARTUP%\TrinityDaemon.bat"

echo SUCCESS: Daemon will start on Windows boot

echo.
echo === DONE ===
echo.
echo Weekly credit burn: Every Sunday at 8 PM
echo Daemon: Starts on Windows boot
echo.
echo To test now:
echo   python .trinity\automation\WEEKLY_CREDIT_BURNER.py
echo   python .trinity\automation\CROSS_COMPUTER_DAEMON.py
echo.
pause
