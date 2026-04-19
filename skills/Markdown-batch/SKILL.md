---
name: Markdown-batch
description: "MarkItDown 批量转换工具：将 Word/PDF/PPT/Excel 批量转换为 Markdown"
tags: markdown,convert,batch
license: MIT
---

# MarkItDown转换

## MarkItDown 工具安装与 GUI 搭建

- 调研了微软开源项目 MarkItDown（https://github.com/microsoft/markitdown），确认可批量将 Word/PDF/PPT/Excel 等转为 Markdown。
- 在本机 Python 环境安装 markitdown 0.0.2。
- 创建了可视化 GUI 工具（Tkinter）：
  - 文件：`c:/Users/markitdown_gui.py`
  - 启动方式：`c:/Users/启动MarkItDown转换工具.bat`
- 功能：单文件/批量文件夹转换、格式下拉选择（Word/PDF/PPT/Excel/HTML/CSV/JSON/XML/TXT）、输出目录选择、子目录递归、覆盖选项、实时日志。
- 场景定位：可作为 Word→Markdown→Remotion 视频工作流的前处理环节。

## markitdown_gui.py 错误处理优化

- 修复：批量转换时遇到 BadZipFile（旧版.doc改名为.docx）会给出友好提示并跳过，不影响其他文件。
- 修复：入口处捕获 KeyboardInterrupt，防止命令行 Ctrl+C 导致 GUI 崩溃。

## 批量 .doc → .docx 转换工具

- 创建了 `doc_to_docx.py` + `启动doc转docx工具.bat`
- 原理：调用本机 Microsoft Word（win32com），后台静默打开.doc另存为.docx
- 功能：GUI 界面、递归子目录、可选输出目录、可选删除原文件、实时日志
- 用途：配合 markitdown_gui.py 前处理，先把旧.doc批量升级为.docx再转Markdown