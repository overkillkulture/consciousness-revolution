@echo off
REM Start Cyclotron Brain Agent as Windows background service
cd /d "C:\Users\darri\100X_DEPLOYMENT"

REM Start with pythonw (no console window)
start "Cyclotron Brain Agent" /B pythonw CYCLOTRON_BRAIN_AGENT.py >> .cyclotron_atoms\brain_agent.log 2>&1

echo Cyclotron Brain Agent started in background
echo Check status with: python CYCLOTRON_BRAIN_AGENT.py status
echo View log: type .cyclotron_atoms\brain_agent.log
