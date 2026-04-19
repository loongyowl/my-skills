@echo off
chcp 65001 >nul
REM ============================================================
REM pdf-to-markdown 依赖安装脚本
REM 自动检测并安装缺失的依赖
REM ============================================================

setlocal EnableDelayedExpansion

set "SKILL_DIR=%~dp0.."
set "DEPS_DIR=%SKILL_DIR%\dependencies"

echo ================================================
echo     PDF转Markdown - 依赖自动安装
echo ================================================
echo.

REM ---- Step 1: 先运行检测 ----
call "%~dp0install_check.bat"
echo.

REM ---- Step 2: 确认是否继续 ----
if !errorlevel!==0 (
    echo 所有依赖已就绪，无需安装。
    pause
    exit /b 0
)

echo 检测到缺失依赖，开始自动安装...
echo.

REM ---- Step 3: 安装 Python 包 ----
echo ================================================
echo [1/2] 安装 Python 包（pymupdf, rapidocr）...
echo ================================================
echo.

echo 正在安装 pymupdf...
pip install pymupdf -q
if !errorlevel!==0 (
    echo   [OK] pymupdf 安装成功
) else (
    echo   [失败] pymupdf 安装失败，请检查 pip
)

echo.
echo 正在安装 rapidocr（扫描件 OCR 用，可选）...
pip install rapidocr-onnxruntime -q
if !errorlevel!==0 (
    echo   [OK] rapidocr 安装成功
) else (
    echo   [失败] rapidocr 安装失败，扫描件 OCR 功能不可用
)

REM ---- Step 4: 安装 OpenDataLoader CLI ----
echo.
echo ================================================
echo [2/2] 安装 OpenDataLoader PDF CLI...
echo ================================================
echo.

echo 正在安装 opendataloader-pdf...
pip install opendataloader-pdf -q
if !errorlevel!==0 (
    echo   [OK] opendataloader-pdf 安装成功
) else (
    echo   [失败] 请手动运行：pip install opendataloader-pdf
)

REM ---- Step 5: JDK 说明 ----
echo.
echo ================================================
echo JDK 21 安装说明
echo ================================================
echo.
echo   JDK 21 需要手动下载安装（包较大，约 300MB）
echo.
echo   下载地址：https://download.java.net/java/GA/jdk21.0.5/fd0bb3b4425a47f2b1ce9f8d3a4e4d9e/0/GPL/openlogic-openjdk-21.0.5+11-windows-x64.zip
echo.
echo   安装后将 JDK 文件夹放到技能包的 dependencies\jdk\ 下
echo   或者放到以下位置之一（会被自动检测）：
echo     - C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64
echo.
echo   检测到 JDK 后，运行一次 install_check.bat 确认状态
echo.

REM ---- Step 6: 最终检测 ----
echo.
echo ================================================
echo     安装完成，重新检测
echo ================================================
call "%~dp0install_check.bat"

pause
