@echo off
chcp 65001 >nul
title MarkItDown 文档转 Markdown 工具

:: 获取脚本所在目录
cd /d "%~dp0"

:: 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10 或更高版本。
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b
)

:: 检查 markitdown，若未安装则自动安装
python -c "import markitdown" >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在自动安装 markitdown，请稍候...
    pip install markitdown -q
    if errorlevel 1 (
        echo [错误] 安装失败，请手动运行：pip install markitdown
        pause
        exit /b
    )
    echo [完成] markitdown 安装成功！
)

:: 启动 GUI
python "%~dp0markitdown_gui.py"

exit /b
