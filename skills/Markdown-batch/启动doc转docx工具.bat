@echo off
chcp 65001 >nul
title 批量 .doc → .docx 转换工具

cd /d "%~dp0"

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b
)

:: 检查 pywin32
python -c "import win32com.client" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 pywin32，请稍候...
    pip install pywin32 -q
    if errorlevel 1 (
        echo [错误] 安装失败，请手动运行：pip install pywin32
        pause
        exit /b
    )
    echo [完成] pywin32 安装成功！
)

:: 启动 GUI
python "%~dp0doc_to_docx.py"

exit /b
