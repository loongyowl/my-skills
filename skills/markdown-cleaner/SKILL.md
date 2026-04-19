---
name: markdown-cleaner
description: Markdown 文件清洗工具。用于处理被错误断行的 Markdown 文件，删除图片引用，合并断行段落。触发词：清洗markdown、markdown排版、删除图片、合并段落、断行修复、清理md文件
author: WorkBuddy
version: "1.0"
tags:
  - markdown
  - text-processing
  - cleanup
license: MIT
---

# Markdown Cleaner

智能清洗被错误断行的 Markdown 文件。

## 功能

1. **合并断行段落** - 将分散的多行合并为完整段落（默认开启）
2. **删除图片引用** - 匹配 `![image](*.png)` 格式（**需询问用户确认后执行**）
3. **保留文档结构** - 标题、列表、分隔线等单独保留
4. **清理多余空行** - 最多保留连续1个空行

## 适用场景

- PDF/扫描件转换的 Markdown 文件
- Word 导出后被错误断行的文件
- 网页抓取后格式混乱的 Markdown
- 需要批量清洗的同类文件

## 使用方法

### 基本用法

```python
from cleanup_markdown import process_markdown

content = open("input.md", "r", encoding="utf-8").read()

# 删除图片（需用户确认）
cleaned = process_markdown(content, remove_images=True)

# 保留图片
cleaned = process_markdown(content, remove_images=False)

open("output.md", "w", encoding="utf-8").write(cleaned)
```

### ⚠️ 图片处理说明

**默认不删除图片**，除非用户明确要求删除图片。执行前必须询问：

> "是否需要删除图片引用？（删除后将无法恢复）"

用户确认后，才能设置 `remove_images=True`。

### 命令行用法

```bash
python cleanup_markdown.py
# 或修改脚本中的 INPUT_FILE 和 OUTPUT_FILE
```

## 算法说明

### 智能合并策略

1. **空行处理**：空行只作为段落分隔信号，不单独添加到结果
2. **累积机制**：短内容（<100字符）继续累积，不急于 flush
3. **句子边界**：以大写字母开头 + 句末标点结尾 = 独立句子，触发 flush
4. **标题识别**：
   - `#` 开头且后面紧跟空行 = 保留为标题
   - 全大写短标题（3-60字符）= 保留为标题
5. **列表保留**：`-`、`*`、`+` 开头的行单独保留
6. **分隔线保留**：`---`、`***`、`___` 等单独保留

### 判断逻辑伪代码

```python
def should_flush_paragraph(current_para, next_line):
    if not current_para:
        return False
    current_text = ' '.join(current_para)
    
    # 段落已有100+字符时，考虑flush
    if len(current_text) >= 100:
        next_stripped = next_line.strip() if next_line else ''
        # 下一行以小写开头 = 句子继续，不flush
        if next_stripped and next_stripped[0].islower():
            return False
        return True
    return False
```

## 依赖

- Python 3.6+
- 无外部依赖（仅使用标准库 re）

## 示例

### 输入示例

```
This is a very long paragraph
that was incorrectly split

across multiple lines

# Title

Another paragraph
here.
```

### 输出示例

```
This is a very long paragraph that was incorrectly split across multiple lines

# Title

Another paragraph here.
```
