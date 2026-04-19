@echo off
chcp 65001 >nul
REM ============================================================
REM pdf-to-markdown 依赖检测脚本
REM 检查 JDK、CLI、Python 包是否已安装
REM ============================================================

setlocal EnableDelayedExpansion

set "SKILL_DIR=%~dp0.."
set "DEPS_DIR=%SKILL_DIR%\dependencies"

echo ================================================
echo     PDF转Markdown - 依赖环境检测
echo ================================================
echo.

set "JAVA_OK=0"
set "CLI_OK=0"
set "PYMUPDF_OK=0"

REM ---- 1. 检测 JDK ----
echo [1/3] 检测 JDK 21...
REM 先检查技能包内
if exist "%DEPS_DIR%\jdk\bin\java.exe" (
    set "JAVA_HOME=%DEPS_DIR%\jdk"
    set "JAVA_HOME_USED=dependencies\jdk"
    set "JAVA_OK=1"
) else (
    REM 检查用户级安装（多种常见路径）
    if exist "C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64\bin\java.exe" (
        set "JAVA_HOME=C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64"
        set "JAVA_HOME_USED=用户级安装（JDK 21）"
        set "JAVA_OK=1"
    ) else (
        REM 尝试从 PATH 中找 java
        for /f "tokens=*" %%i in ('where java 2^>nul') do (
            if !JAVA_OK!==0 (
                set "JAVA_HOME=%%~dpi"
                set "JAVA_HOME=!JAVA_HOME:~0,-5!"
                set "JAVA_HOME_USED=系统 PATH"
                java -version 2>&1 | findstr /i "version" >nul
                if !errorlevel!==0 set "JAVA_OK=1"
            )
        )
    )
)

if "!JAVA_OK!"=="1" (
    echo   [OK] JDK 已找到：!JAVA_HOME_USED!
) else (
    echo   [缺失] JDK 21 未安装
)

REM ---- 2. 检测 OpenDataLoader CLI ----
echo.
echo [2/3] 检测 OpenDataLoader PDF CLI...
REM 先检查技能包内
if exist "%DEPS_DIR%\opendataloader-pdf.exe" (
    set "CLI=%DEPS_DIR%\opendataloader-pdf.exe"
    set "CLI_USED=dependencies"
    set "CLI_OK=1"
) else (
    REM 检查用户 PATH
    for /f "tokens=*" %%i in ('where opendataloader-pdf.exe 2^>nul') do (
        if !CLI_OK!==0 (
            set "CLI=%%i"
            set "CLI_USED=系统 PATH"
            set "CLI_OK=1"
        )
    )
)

if "!CLI_OK!"=="1" (
    echo   [OK] CLI 已找到：!CLI_USED!
) else (
    echo   [缺失] opendataloader-pdf.exe 未安装
)

REM ---- 3. 检测 Python 包 ----
echo.
echo [3/3] 检测 Python 包（pymupdf, rapidocr）...

REM pymupdf
python -c "import pymupdf" 2>nul
if !errorlevel!==0 (
    for /f "tokens=*" %%v in ('python -c "import pymupdf; print(pymupdf.__version__)"') do set "PYMUPDF_VER=%%v"
    echo   [OK] pymupdf !PYMUPDF_VER!
) else (
    echo   [缺失] pymupdf
)

REM rapidocr
python -c "import rapidocr_onnxruntime" 2>nul
if !errorlevel!==0 (
    echo   [OK] rapidocr
) else (
    echo   [缺失] rapidocr-onnxruntime（扫描件 OCR 用）
)

REM ---- 汇总报告 ----
echo.
echo ================================================
if "!JAVA_OK!"=="1" if "!CLI_OK!"=="1" (
    echo 状态：所有必需依赖已就绪，可以直接使用
    exit /b 0
) else (
    echo 状态：部分依赖缺失，请运行 install_dependencies.bat 安装
    exit /b 1
)
