@echo off
echo Setting up daily cleanup task...

schtasks /create /tn "PC1_Daily_Cleanup" /tr "C:\Users\dwrek\PC1_LOCAL_HUB\RUN_DAILY_CLEANUP.bat" /sc daily /st 03:00 /f

echo.
echo Task scheduled: PC1_Daily_Cleanup
echo Runs daily at 3:00 AM
echo.
echo To check: schtasks /query /tn "PC1_Daily_Cleanup"
echo To delete: schtasks /delete /tn "PC1_Daily_Cleanup" /f
