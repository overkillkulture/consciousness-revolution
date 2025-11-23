@echo off
echo ========================================
echo PC1 DAILY CLEANUP - %date% %time%
echo ========================================

cd /d C:\Users\dwrek

echo.
echo Running maintenance daemon...
python PC1_LOCAL_HUB\MAINTENANCE_DAEMON.py

echo.
echo Running git branch cleanup...
cd 100X_DEPLOYMENT
git branch --merged master | findstr /v "master main" > temp_branches.txt
for /f %%i in (temp_branches.txt) do git branch -d %%i
del temp_branches.txt
git fetch --prune

echo.
echo Cleanup complete!
echo ========================================
