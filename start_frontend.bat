@echo off
echo ========================================
echo Starting Frontend Development Server
echo ========================================
echo.

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
)

echo.
echo Starting frontend development server...
echo The app will open at http://localhost:5173
echo Press CTRL+C to stop the server
echo.

REM Start the dev server
call npm run dev

pause
