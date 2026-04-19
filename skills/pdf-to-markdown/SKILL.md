---
name: pdf-to-markdown
description: 将 PDF 文件转换为 Markdown 格式。支持原生文本 PDF（OpenDataLoader PDF）和扫描版 PDF（RapidOCR 离线 OCR）。可单文件或批量转换，适合导入 Obsidian 知识库或喂给 AI/RAG 系统。
trigger:
  - "PDF转Markdown"
  - "PDF转md"
  - "转换PDF"
  - "pdf convert"
  - "pdf2md"
  - "PDF 批量转换"
  - "扫描版 PDF OCR"
license: MIT
---

# PDF 转 Markdown 技能

## 技能包文件结构

```
pdf-to-markdown/
├── SKILL.md                        # 本文件（技能说明）
├── scripts/
│   ├── pdf_convert.bat             # 命令行调用入口（被菜单 bat 调用）
│   ├── pdf转换工具.bat              # 双击交互菜单（用户直接使用）
│   ├── install_check.bat           # AI 用：检测依赖是否已安装
│   ├── install_dependencies.bat    # AI 用：检测后自动安装缺失依赖
│   ├── convert_single.py           # 单文件转换
│   ├── batch_convert.py            # 批量转换
│   └── check_pdf_type.py           # 检测 PDF 类型
├── dependencies/                   # 可选：将 JDK 和 CLI 打包到此处
│   ├── jdk/                        # OpenJDK 21（手动放入，节省下载时间）
│   └── opendataloader-pdf.exe      # CLI（手动放入，节省 pip 安装）
└── references/
    └── usage_examples.md           # 使用示例
```

> **依赖回退机制**：若 `dependencies/` 目录下无对应文件，所有脚本自动回退到用户机器上已安装的路径，无需手动修改代码。

---

## AI 安装引导（给其他 AI 智能体使用）

> **重要原则**：在任何操作之前，**必须先运行检测**，已安装的依赖不得重复安装。

### 原则一：先检测，再安装

本技能包包含两个检测脚本，同一台机器只需运行一次：

```
scripts\install_check.bat        # 只检测，不安装
scripts\install_dependencies.bat # 检测后自动安装缺失项
```

### 原则二：本机已安装则跳过

检测脚本会按以下顺序查找依赖，**找到即停止**：

| 依赖 | 检测顺序（找到即用） |
|------|---------------------|
| JDK | ① `dependencies/jdk/` → ② `C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64` → ③ 系统 PATH 中的 java |
| OpenDataLoader CLI | ① `dependencies/opendataloader-pdf.exe` → ② 系统 PATH 中的 opendataloader-pdf.exe |
| pymupdf | Python 库（pip show pymupdf） |
| rapidocr | Python 库（pip show rapidocr-onnxruntime） |

### AI 调用流程

当其他 AI 智能体收到用户的 PDF 转换请求时，**按以下步骤执行**：

**Step 1：检测依赖**
```batch
scripts\install_check.bat
```
读取输出：
- 显示 "所有必需依赖已就绪" → 直接跳到 Step 3
- 显示 "部分依赖缺失" → 继续 Step 2

**Step 2：安装缺失依赖**
```batch
scripts\install_dependencies.bat
```
脚本会自动：
- ✅ pip install pymupdf（若缺失）
- ✅ pip install rapidocr-onnxruntime（若缺失，可选）
- ✅ pip install opendataloader-pdf（若缺失）
- ⚠️ JDK 21 需要手动下载（约 300MB），脚本会给出下载地址

**Step 3：执行转换**
```batch
scripts\pdf_convert.bat "PDF路径" markdown "输出目录"
```
或使用 Python 脚本：
```powershell
python scripts\batch_convert.py "PDF目录" "输出目录"
```

### 安装状态文件（供 AI 记忆）

检测结果不依赖文件存储，每次运行时自动检测。若 AI 需要判断当前状态，可直接调用 `install_check.bat` 并检查 exit code：
- `exit /b 0` → 依赖就绪
- `exit /b 1` → 需安装

---

## 工具链

| 工具 | 用途 | 优先路径 | 回退路径 |
|------|------|----------|----------|
| OpenDataLoader PDF CLI | 原生文本 PDF → Markdown/JSON | `dependencies/opendataloader-pdf.exe` | `%AppData%\Python\Python314\Scripts\opendataloader-pdf.exe` |
| OpenJDK 21 | OpenDataLoader 底层依赖 | `dependencies/jdk/` | `C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64` |
| pdf_convert.bat | 命令行快捷入口 | `scripts/pdf_convert.bat` | — |
| pdf转换工具.bat | 双击交互菜单 | `scripts/pdf转换工具.bat` | — |
| RapidOCR | 扫描版 PDF 离线 OCR | Python 库（pip install rapidocr-onnxruntime） | — |
| PyMuPDF | PDF 类型检测 + 损坏修复 | Python 库（pip install pymupdf） | — |

---

## 使用方式

### 方式 1：双击菜单（推荐）

双击 `scripts/pdf转换工具.bat`，按提示选择模式：

```
================================================
         PDF 转换工具  (by Claw)
================================================
  1. 转换单个 PDF -- 输出 Markdown (适合 Obsidian)
  2. 批量转换文件夹 -- 输出 Markdown
  3. 批量转换文件夹 -- 输出 JSON (适合 AI)
  4. AI 混合模式 (扫描件/表格/公式效果更好)
  0. 退出
```

### 方式 2：命令行调用

```powershell
# 单文件
scripts\pdf_convert.bat "D:\文档.pdf" markdown "D:\输出\"

# 批量目录
scripts\pdf_convert.bat "D:\PDF目录\" markdown "D:\输出\"

# JSON 格式
scripts\pdf_convert.bat "D:\PDF目录\" json "D:\输出\"
```

### 方式 3：Python 脚本

```powershell
# 单文件
python scripts\convert_single.py "D:\文档.pdf" "D:\输出\"

# 批量转换
python scripts\batch_convert.py "D:\PDF目录\" "D:\输出\"

# 检测 PDF 类型
python scripts\check_pdf_type.py "D:\文档.pdf"
```

---

## 工作流程

### Step 1：判断 PDF 类型

用 PyMuPDF 抽取前几页文本：
- **每页 > 50 字** → 原生文本 PDF → 用 OpenDataLoader
- **每页 < 30 字** → 扫描版 PDF → 用 RapidOCR

```python
# scripts/check_pdf_type.py
python scripts\check_pdf_type.py "D:\文档.pdf"
# 输出示例：原生文本 PDF | 320页 | 均字量:1247 | 文档.pdf
```

### Step 2a：原生文本 PDF → Markdown

```powershell
$env:JAVA_HOME = "SKILL根目录\dependencies\jdk"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
$cli = "SKILL根目录\dependencies\opendataloader-pdf.exe"
& $cli "PDF路径" -f markdown -o "输出目录"
```

**参数格式注意**：CLI v2 使用 `-f format -o output_dir`，不是位置参数。

### Step 2b：扫描版 PDF → OCR

```powershell
# 用 scripts/scan_pdf_ocr.py（需安装 rapidocr-onnxruntime）
python scripts\scan_pdf_ocr.py "PDF路径" "输出目录"
```

---

## 已知问题

### 封面/目录标题汉字间有空格
- **原因**：PDF 字符间距（kerning）特性，OpenDataLoader 忠实还原了原始间距
- **影响**：仅封面/目录页，正文无此问题
- **处理**：Obsidian 导入后手动修复，或正则替换 `(?<=[\u4e00-\u9fa5]) (?=[\u4e00-\u9fa5])` → `""`

### PDF xref 损坏
- **原因**：PDF 文件本身损坏
- **处理**：用 PyMuPDF 修复后再转换：
  ```python
  import pymupdf
  doc = pymupdf.open("损坏.pdf")
  doc.save("修复后.pdf", garbage=4, deflate=True)
  doc.close()
  ```

---

## 输出说明

- Markdown 输出到指定目录（或 PDF 同目录）
- 图片单独存入 `{原文件名}_images/` 子目录
- JSON 格式（含边界框）用 `-f json` 参数

---

## 参考文件

- `references/usage_examples.md` - 实际使用示例
