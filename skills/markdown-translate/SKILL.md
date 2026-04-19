---
name: markdown-translate
description: "批量翻译 Markdown 文件，保持格式完整，支持多 API (DeepSeek/OpenAI/自定义)，断点续传，Tkinter 可视化界面。"
license: MIT
---

# Markdown 批量翻译工具

## 功能

- 支持单个文件或文件夹批量翻译
- 保持 Markdown 格式（代码块、引用、标题、加粗/斜体、链接、数学公式、脚注）
- 多 API 支持：DeepSeek / OpenAI / 任意 OpenAI 兼容 API
- 断点续传：中断后跳过已翻译文件
- 暂停/继续/停止控制
- Tkinter 可视化界面

## 启动

```bash
pip install openai
python skills/markdown-translate/scripts/app.py
```

## 使用流程

1. 选择 API 并填写 Key / URL / Model
2. 选择 MD 文件夹
3. 点击"开始翻译"
4. 翻译后文件保存为 `原名.translated.md`，在同目录下

## 输出示例

```
原文件:   books/meditations.md
翻译后:   books/meditations.translated.md
```

##  # Search for a skillskills-cli search <keyword>​# Install a skillskills-cli install <skill-name>bash

| 文件 | 用途 |
|------|------|
| `scripts/app.py` | Tkinter 界面 |
| `scripts/translator.py` | 翻译引擎 (API 调用/分块/断点续传) |
| `scripts/markdown_parser.py` | 格式保护与还原 |
| `scripts/config.json` | API 配置 (自动生成) |

## 格式保护策略

翻译前提取 Markdown 语法替换为占位符，翻译后还原：

```
**加粗** → ___BOLD_1___ → 翻译 → ___BOLD_1___ → **加粗**
`代码`   → ___CODE_INLINE_1___ → 翻译 → ___CODE_INLINE_1___ → `代码`
```

支持保护的语法：代码块、行内代码、数学公式、链接、图片、脚注、加粗、斜体

## 断点续传

每个文件夹下自动生成 `.translate_manifest.json`，记录已翻译文件的 SHA-256 哈希。重跑时自动跳过未修改的已翻译文件。
