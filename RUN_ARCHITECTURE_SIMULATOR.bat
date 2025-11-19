@echo off
REM Multi-AI Architecture Simulator - Quick Launch
REM Auto-navigates to script directory and runs simulation

cd /d "%~dp0"
echo.
echo ========================================
echo   MULTI-AI ARCHITECTURE SIMULATOR
echo ========================================
echo.
echo Running simulation...
echo.

python ARCHITECTURE_SIMULATOR.py

echo.
echo ========================================
echo   SIMULATION COMPLETE
echo ========================================
echo.
echo Results saved to:
echo   - ARCHITECTURE_SIMULATION_RESULTS.json
echo   - AI_ARCHITECTURE_RECOMMENDATIONS.md
echo.
echo To view dashboard: Open ARCHITECTURE_SIMULATOR_DASHBOARD.html in browser
echo To view wiring: Open DATA_WIRING_DIAGRAM.html in browser
echo.
pause
