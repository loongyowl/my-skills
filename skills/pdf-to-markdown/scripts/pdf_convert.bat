@echo off
REM OpenDataLoader PDF 快捷启动脚本 v3
REM 路径自动基于本脚本所在位置解析，无需修改
REM
REM 用法:
REM   pdf_convert <pdf文件或文件夹> [输出格式] [输出目录]
REM 输出格式: markdown  json  text  html  markdown-with-images
REM 示例:
REM   pdf_convert "D:\文档.pdf" markdown "D:\输出\"
REM   pdf_convert "D:\文件夹\" json "D:\输出\"

REM --- 自动定位技能包根目录（scripts 的上一级）---
set "SKILL_DIR=%~dp0.."

set "JAVA_HOME=%SKILL_DIR%\dependencies\jdk"
set "PATH=%JAVA_HOME%\bin;%PATH%"
set "CLI=%SKILL_DIR%\dependencies\opendataloader-pdf.exe"

REM --- 若 dependencies 内没有 exe，回退到用户级安装路径 ---
if not exist "%CLI%" (
    set "CLI=C:\Users\JoeHuang\AppData\Roaming\Python\Python314\Scripts\opendataloader-pdf.exe"
    set "JAVA_HOME=C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64"
    set "PATH=%JAVA_HOME%\bin;%PATH%"
)

if "%~1"=="" (
    echo 用法: pdf_convert ^<pdf文件或文件夹^> [输出格式] [输出目录]
    echo.
    echo 输出格式: markdown  json  text  html  markdown-with-images
    echo 默认格式: markdown
    echo.
    echo 示例:
    echo   pdf_convert "D:\文档.pdf" markdown "D:\输出\"
    echo   pdf_convert "D:\文件夹\" json "D:\输出\"
    exit /b 1
)

set "INPUT=%~1"
set "FMT=markdown"
set "OUTDIR="

if not "%~2"=="" set "FMT=%~2"
if not "%~3"=="" set "OUTDIR=%~3"

if "%OUTDIR%"=="" (
    "%CLI%" "%INPUT%" -f "%FMT%"
) else (
    "%CLI%" "%INPUT%" -f "%FMT%" -o "%OUTDIR%"
)
