@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

REM --- 自动定位技能包根目录（scripts 的上一级）---
set "SKILL_DIR=%~dp0.."
set "SCRIPTS_DIR=%~dp0"

:MAIN_MENU
cls
echo ================================================
echo          PDF 转换工具  (by Claw)
echo ================================================
echo.
echo   1. 转换单个 PDF -- 输出 Markdown (适合 Obsidian)
echo   2. 批量转换文件夹 -- 输出 Markdown
echo   3. 批量转换文件夹 -- 输出 JSON (适合 AI)
echo   4. AI 混合模式 (扫描件/表格/公式效果更好)
echo   0. 退出
echo.
echo ================================================
echo.
set /p CHOICE=请选择操作 [0-4]：

if "%CHOICE%"=="1" goto SINGLE_MD
if "%CHOICE%"=="2" goto BATCH_MD
if "%CHOICE%"=="3" goto BATCH_JSON
if "%CHOICE%"=="4" goto HYBRID_MD
if "%CHOICE%"=="0" goto EXIT
echo 无效选项，请重新选择。
pause
goto MAIN_MENU

:: -------------------------------------------------
:SINGLE_MD
cls
echo ================================================
echo        模式 1：单个 PDF 转 Markdown
echo ================================================
echo.
echo   适用场景：单本书籍、单份文件转换
echo   输出格式：.md 文件，可直接导入 Obsidian
echo.
echo   提示：可把文件直接拖入此窗口自动填入路径
echo.
set /p INPUT_PATH=请输入 PDF 文件路径：
set /p OUTPUT_PATH=请输入输出目录路径（如 D:\output）：
echo.
echo 正在转换，请稍候...
echo.
call "%SCRIPTS_DIR%pdf_convert.bat" "%INPUT_PATH%" markdown "%OUTPUT_PATH%"
echo.
echo [完成] 输出目录：%OUTPUT_PATH%
echo.
pause
goto MAIN_MENU

:: -------------------------------------------------
:BATCH_MD
cls
echo ================================================
echo        模式 2：批量文件夹转 Markdown
echo ================================================
echo.
echo   适用场景：整个文件夹内所有 PDF 批量转换
echo   输出格式：每个 PDF 对应一个 .md 文件
echo.
echo   提示：可把文件夹直接拖入此窗口自动填入路径
echo.
set /p INPUT_PATH=请输入包含 PDF 的文件夹路径：
set /p OUTPUT_PATH=请输入输出目录路径（如 D:\output）：
echo.
echo 正在批量转换，请稍候...
echo.
call "%SCRIPTS_DIR%pdf_convert.bat" "%INPUT_PATH%" markdown "%OUTPUT_PATH%"
echo.
echo [完成] 输出目录：%OUTPUT_PATH%
echo.
pause
goto MAIN_MENU

:: -------------------------------------------------
:BATCH_JSON
cls
echo ================================================
echo        模式 3：批量文件夹转 JSON
echo ================================================
echo.
echo   适用场景：需要把内容喂给 AI 分析时使用
echo   输出格式：每个 PDF 对应一个 .json 文件
echo.
echo   提示：可把文件夹直接拖入此窗口自动填入路径
echo.
set /p INPUT_PATH=请输入包含 PDF 的文件夹路径：
set /p OUTPUT_PATH=请输入输出目录路径（如 D:\output）：
echo.
echo 正在批量转换，请稍候...
echo.
call "%SCRIPTS_DIR%pdf_convert.bat" "%INPUT_PATH%" json "%OUTPUT_PATH%"
echo.
echo [完成] 输出目录：%OUTPUT_PATH%
echo.
pause
goto MAIN_MENU

:: -------------------------------------------------
:HYBRID_MD
cls
echo ================================================
echo        模式 4：AI 混合模式
echo ================================================
echo.
echo   适用场景：
echo     - 扫描版 PDF（图片式，普通模式识别差）
echo     - 含复杂表格的文件
echo     - 含数学公式的文件
echo   输出格式：.md 文件
echo   注意：此模式速度较慢，请耐心等待
echo.
echo   提示：可把文件或文件夹拖入此窗口自动填入路径
echo.
set /p INPUT_PATH=请输入 PDF 文件或文件夹路径：
set /p OUTPUT_PATH=请输入输出目录路径（如 D:\output）：
echo.
echo 正在使用 AI 混合模式转换，请稍候...
echo.
call "%SCRIPTS_DIR%pdf_convert.bat" "%INPUT_PATH%" markdown "%OUTPUT_PATH%" --hybrid docling-fast
echo.
echo [完成] 输出目录：%OUTPUT_PATH%
echo.
pause
goto MAIN_MENU

:: -------------------------------------------------
:EXIT
echo.
echo 再见！
timeout /t 1 >nul
exit
