# PDF 转 Markdown 实际使用示例

## 单文件转换

```powershell
# 方法1：直接用 CLI
$env:JAVA_HOME = "C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64"
$env:PATH = "$env:JAVA_HOME\bin;" + $env:PATH
$cli = "C:\Users\JoeHuang\AppData\Roaming\Python\Python314\Scripts\opendataloader-pdf.exe"
& $cli "D:\文档\文件.pdf" -f markdown -o "D:\输出目录\"
```

```powershell
# 方法2：用 Python 脚本
python C:\Users\JoeHuang\.workbuddy\skills\pdf-to-markdown\scripts\convert_single.py "D:\文档\文件.pdf" "D:\输出目录\"
```

```cmd
# 方法3：用 bat 快捷命令（需在新开的命令行窗口）
pdf_convert "D:\文档\文件.pdf" markdown "D:\输出目录\"
```

## 批量转换

```powershell
# 转换目录下所有 PDF
python C:\Users\JoeHuang\.workbuddy\skills\pdf-to-markdown\scripts\batch_convert.py "D:\PDF目录\" "D:\输出目录\"
```

## 检测 PDF 类型

```powershell
python C:\Users\JoeHuang\.workbuddy\skills\pdf-to-markdown\scripts\check_pdf_type.py "D:\文档\文件.pdf"
```

输出示例：
- `原生文本 PDF | 328页 | 均字量:1200 | 禅与摩托车维修艺术.pdf`
- `扫描版 PDF | 64页 | 均字量:12 | GJBZ141-2004.pdf`

## 扫描版 PDF 处理

如果检测为扫描版，用 RapidOCR（需先确认已安装）：

```powershell
python C:\Users\JoeHuang\WorkBuddy\Claw\rapid_ocr_batch.py "D:\扫描版.pdf" "D:\输出目录\"
```

## 修复损坏的 PDF

```python
import pymupdf
doc = pymupdf.open("损坏的.pdf")
doc.save("修复后.pdf", garbage=4, deflate=True)
doc.close()
```

## JSON 格式输出（带边界框）

```powershell
& $cli "D:\文档\文件.pdf" -f json -o "D:\输出目录\"
```

## 修复封面标题空格问题

如果封面标题出现 `禅 摩 托 维 修 艺 术`（汉字间空格），在 Obsidian 中用正则替换：

```
查找: (?<=[\u4e00-\u9fa5]) (?=[\u4e00-\u9fa5])
替换: (留空)
```

或在 VSCode/Notepad++ 中：
```
查找: ([一-龥])\s+([一-龥])
替换: \1\2
```
