@echo off
chcp 65001 >nul
cd /d "%~dp0"
python scripts\pack.py incoming ready
pause
