@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if activation worked
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    echo Make sure you're in the project root directory.
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Install dependencies if needed (optional check)
echo Checking dependencies...
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting FastAPI server on http://localhost:8000
echo Press CTRL+C to stop the server
echo.

REM Start the server
uvicorn backend.app.main:app --reload --port 8000

pause
