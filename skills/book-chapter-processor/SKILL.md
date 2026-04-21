---
name: book-chapter-processor
description: "Use this skill when working with book-chapter-processor."
license: MIT
---

---
name: book-chapter-processor
description: "高保真书籍章节加工器：将书籍片段通过 LLM 加工成 Obsidian 风格的 Markdown 笔记。支持 DeepSeek、OpenAI、Claude、Gemini 等多 API 提供商，提供 5 种预设提示词模板。"
license: MIT
---

# 高保真书籍章节加工器

一个基于 React 的单页面应用，用于将精读的书籍片段加工成符合 Obsidian 审美的高保真 Markdown 笔记。

在线使用：https://loongyowl.github.io/book-chapter-processor/

## 功能特性

快速整理书籍章节，自动转为不同的笔记类型，可本地或云端运行，方便快捷。

- **多 API 支持**：DeepSeek（默认）、OpenAI、Anthropic Claude、Google Gemini、自定义
- **5 种提示词模板**：
  - 深度笔记：保留原文、案例、金句
  - 简洁大纲：提取核心观点，省略案例
  - 金句摘录：突出原文引用，金句加粗
  - 思维导图：层级结构，bullet points
  - 问答笔记：转化为自问自答形式
- **自定义提示词**：可手动编辑覆盖预设模板
- **渲染/源码双视图**：支持切换查看和编辑
- **YAML Frontmatter 自动生成**：包含书名、作者、章节、日期
- **一键复制和下载**：导出为 .md 文件

## 安装方法

### 方式一：使用一键启动脚本（推荐）

项目已提供两个批处理文件，双击即可运行：

| 文件 | 用途 | 特点 |
|:---|:---|:---|
| `启动开发服务器.bat` | 开发模式 | 热重载，修改代码自动刷新，适合开发调试 |
| `启动预览模式.bat` | 生产预览 | 先构建再预览，模拟真实部署效果 |

**使用方法**：
1. 进入 `book-chapter-processor` 文件夹
2. 双击 `启动开发服务器.bat` 或 `启动预览模式.bat`
3. 自动打开浏览器访问 http://localhost:5174或http://localhost:4173/

**注意事项**：
- 确保已安装 Node.js（建议 v18+）
- 首次运行会自动安装依赖
- 预览模式会先执行 `npm run build`，稍等片刻

### 方式二：命令行模式

```bash
cd skills/book-chapter-processor
npm install
npm run dev
```

启动后访问 http://localhost:5174

### 方式三：生产构建

```bash
cd skills/book-chapter-processor
npm install
npm run build
npm run preview
```

构建产物在 dist/ 目录，可部署到任意静态服务器。

### 方式四：部署到静态服务器

将 dist/ 目录部署到：
- GitHub Pages
- Vercel
- Netlify
- 本地 HTTP 服务器

## 使用说明

### 1. 配置 API

点击顶部「API设置」按钮：
- 选择 LLM 提供商（默认 DeepSeek）
- 输入 API Key
- 确认 Base URL 和模型名称
- 点击「测试连接」验证

### 2. 填写元数据

在顶部输入框填写：
- 书名（自动格式化为 [[书名]]）
- 作者
- 章节名（用于文件名）

### 3. 选择模板

点击「模板」按钮选择提示词模板，或输入自定义提示词。

### 4. 输入原始文本

在左侧「原始文本」区域粘贴书籍片段。

### 5. 开始加工

点击底部「开始加工」按钮，等待 LLM 处理完成。

### 6. 编辑和导出

- 在右侧「渲染」视图查看效果
- 切换到「源码」视图直接编辑 Markdown
- 点击「复制」或「下载」导出结果

## 技术栈

- React 18 + Vite
- Tailwind CSS
- Monaco Editor（VS Code 同款编辑器）
- react-markdown（Markdown 渲染）
- Lucide React（图标）

## 文件结构

`
book-chapter-processor/
├── SKILL.md                # 本文档
├── package.json            # 依赖配置
├── vite.config.js          # Vite 配置
├── tailwind.config.js      # Tailwind 配置
├── index.html              # 入口 HTML
├── src/
│   ├── main.jsx            # React 入口
│   ├── index.css           # 样式
│   ├── App.jsx             # 主组件
│   ├── components/         # UI 组件
│   ├── hooks/              # 自定义 hooks
│   ├── constants/          # 常量配置
│   └── utils/              # 工具函数
└── dist/                   # 构建输出
`

## 注意事项

1. API Key 会保存在浏览器 localStorage，请勿在公共电脑上保存敏感信息
2. 长文本处理可能需要较长时间，请耐心等待
3. 建议使用 DeepSeek 等性价比高的 API 提供商
4. 输出结果可手动编辑调整

## 更新日志

### v1.1.0 (2026-04-21)

- **SettingsModal 自动保存**：按 ESC 键或点击遮罩关闭时自动保存设置，无需手动点保存
- **请求超时保护**：添加 2 分钟请求超时，防止长时间无响应
- **增加 max_tokens**：从 4096 提升到 8192，支持更长输出
- **进度提示优化**：处理中显示"请耐心等待"提示

### v1.0.0 (2026-04-20)

- 初始版本发布
- 支持 5 种提示词模板
- 支持多 API 提供商
- 渲染/源码双视图
- 自动生成 YAML Frontmatter
