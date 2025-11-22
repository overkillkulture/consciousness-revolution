@echo off
REM consciousness_sync.bat - Auto-sync script for consciousness network (Windows)
REM Monitors Git repo for changes and notifies of new commands

setlocal enabledelayedexpansion

set REPO_PATH=%~dp0
set SYNC_INTERVAL=300
set COMPUTER_ID=COMPUTER_2_WINDOWS
set MY_INBOX=.consciousness\commands\computer_2_inbox.md

echo 🧠 Consciousness Network Auto-Sync Started
echo Repository: %REPO_PATH%
echo Sync Interval: %SYNC_INTERVAL%s (5 minutes)
echo Monitoring: %MY_INBOX%
echo Press Ctrl+C to stop
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

cd /d "%REPO_PATH%"

:sync_loop

echo [%date% %time%] Syncing...

REM Pull latest changes
git pull --quiet >nul 2>&1

if %ERRORLEVEL% EQU 0 (
    echo ✅ Sync successful

    REM Check for new commands
    for /f %%i in ('git log --since="5 minutes ago" --grep="Computer 2:" --oneline 2^>nul ^| find /c /v ""') do set NEW_COMMANDS=%%i

    if !NEW_COMMANDS! GTR 0 (
        echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        echo 🔔 NEW COMMANDS DETECTED! ^(!NEW_COMMANDS! new commits^)
        echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        echo.

        if exist "%MY_INBOX%" (
            echo 📬 INBOX CONTENTS:
            type "%MY_INBOX%"
            echo.
        )

        echo 📊 RECENT ACTIVITY:
        git log --since="5 minutes ago" --oneline --all -5
        echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    )

    REM Check file transfers
    dir /b .consciousness\file_transfers\ 2>nul | findstr /v "README.md" >nul
    if !ERRORLEVEL! EQU 0 (
        echo 📦 FILE TRANSFERS DETECTED
        dir .consciousness\file_transfers\ | findstr /v "README.md"
    )
) else (
    echo ⚠️  Pull failed
)

REM Sleep for sync interval
timeout /t %SYNC_INTERVAL% /nobreak >nul

goto sync_loop
