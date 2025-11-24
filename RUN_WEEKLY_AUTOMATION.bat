@echo off
REM ============================================
REM WEEKLY AUTOMATION RUNNER
REM Full weekly maintenance cycle
REM ============================================

echo ============================================
echo    CONSCIOUSNESS REVOLUTION
echo    Weekly Automation Runner
echo ============================================
echo.

cd /d C:\Users\dwrek\100X_DEPLOYMENT

REM Run daily automation first
call RUN_DAILY_AUTOMATION.bat

echo.
echo ============================================
echo WEEKLY TASKS
echo ============================================
echo.

REM Generate scorecard report
echo [WEEKLY] Generating scorecard report...
python SCORECARD_AUTOMATOR.py report
echo.

REM Generate L10 agenda
echo [WEEKLY] Generating L10 agenda...
python L10_MEETING_AUTOMATION.py agenda
echo.

REM Show todo reminders
echo [WEEKLY] Checking todo reminders...
python L10_MEETING_AUTOMATION.py reminders
echo.

REM Git commit automation changes
echo [WEEKLY] Committing changes to git...
cd /d C:\Users\dwrek\100X_DEPLOYMENT
git add .planning/
git add .consciousness/
git commit -m "Weekly automation run - %date%"
echo.

echo ============================================
echo WEEKLY AUTOMATION COMPLETE
echo ============================================
echo.
echo Ready for L10 meeting!
echo Agenda: .planning\traction\L10_AGENDA_*.md
echo.

pause
