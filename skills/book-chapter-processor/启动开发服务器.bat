@echo off
title Book Chapter Processor
cd /d "%~dp0"
echo ========================================
echo   Book Chapter Processor - Dev Server
echo ========================================
echo.
echo Starting dev server...
start http://127.0.0.1:5174
npm run dev -- --port 5174 --host
