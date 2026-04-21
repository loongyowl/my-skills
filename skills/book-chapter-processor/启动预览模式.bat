@echo off
title Book Chapter Processor - Preview
cd /d "%~dp0"
echo ========================================
echo   Book Chapter Processor - Preview Mode
echo ========================================
echo.

echo Building project...
call npm run build
if errorlevel 1 (
    echo.
    echo [ERROR] Build failed! Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Starting preview server on http://localhost:4173
echo Press Ctrl+C to stop the server.
echo.

:: Delay opening browser (wait 2 seconds then open)
start "" cmd /c "ping -n 3 127.0.0.1 >nul && start http://localhost:4173"

call npm run preview -- --port 4173 --host

pause
