@echo off
REM ============================================
REM DAILY AUTOMATION RUNNER
REM Runs all Consciousness Revolution automation
REM ============================================

echo ============================================
echo    CONSCIOUSNESS REVOLUTION
echo    Daily Automation Runner
echo ============================================
echo.
echo Time: %date% %time%
echo.

cd /d C:\Users\dwrek\100X_DEPLOYMENT

REM 1. Update Scorecard
echo [1/5] Updating scorecard...
python SCORECARD_AUTOMATOR.py
if %errorlevel% neq 0 (
    echo ERROR: Scorecard update failed
) else (
    echo SUCCESS: Scorecard updated
)
echo.

REM 2. Rotate temporal data
echo [2/5] Rotating temporal data...
python TEMPORAL_DATA_ROTATION.py
if %errorlevel% neq 0 (
    echo ERROR: Data rotation failed
) else (
    echo SUCCESS: Data rotated
)
echo.

REM 3. Extract entities for GraphRAG
echo [3/5] Extracting entities...
python GRAPHRAG_ENTITY_EXTRACTOR.py
if %errorlevel% neq 0 (
    echo ERROR: Entity extraction failed
) else (
    echo SUCCESS: Entities extracted
)
echo.

REM 4. Prepare L10 materials
echo [4/5] Preparing L10 materials...
python L10_MEETING_AUTOMATION.py prepare
if %errorlevel% neq 0 (
    echo ERROR: L10 prep failed
) else (
    echo SUCCESS: L10 prepared
)
echo.

REM 5. Knowledge capture test
echo [5/5] Testing knowledge capture...
python KNOWLEDGE_CAPTURE_PIPELINE.py
if %errorlevel% neq 0 (
    echo ERROR: Knowledge capture failed
) else (
    echo SUCCESS: Knowledge captured
)
echo.

echo ============================================
echo AUTOMATION COMPLETE
echo ============================================
echo.
echo Results saved to:
echo   - Scorecard: .planning\traction\SCORECARD_WEEKLY.json
echo   - Archives:  .archives\
echo   - Entities:  .consciousness\graphrag\
echo   - L10 Prep:  .planning\traction\L10_PREP_*.json
echo   - Knowledge: .consciousness\brain\
echo.

pause
