---
name: skill-packager
description: "统一不同来源skills的格式，确保安装后可直接使用。当用户需要审核、标准化、打包来自不同AI智能体的skills时使用。触发词：skill审核、skill标准化、skill打包、skills格式统一、skill补全依赖。"
license: MIT
---

# Skill Packager

将不同AI智能体创建的skills标准化，确保他人安装后能直接使用。

## 快速使用

### 一键打包

双击 `pack-skills.bat` 即可完成全部流程：

```
扫描 → 审核 → 补全 → 测试 → 输出
```

### 手动步骤

```bash
python scripts/pack.py incoming ready
```

## 目录说明

```
skill-packager/
├── incoming/          ← 放入原始skills
├── ready/             ← 输出标准化skills
├── pack-skills.bat    ← 一键打包脚本
├── SKILL.md           # 本文件
├── scripts/
│   ├── scan.py        # 扫描incoming目录
│   ├── audit.py       # 审核完整性
│   ├── fix.py         # 补全缺失文件
│   ├── test.py        # 测试可用性
│   └── pack.py        # 一键打包
├── references/
│   └── templates.md   # 标准模板参考
└── assets/
    ├── LICENSE_MIT.txt
    └── skill_template.md
```

## 使用流程

### 1. 放入原始skills

将待处理的skills放入 `incoming/` 目录：

- 可以是单个 `.md` 文件
- 可以是不完整的skill目录
- 支持多个skill同时处理

```
incoming/
├── pdf-reader.md        ← 单文件
├── data-cleaner/        ← 目录形式
│   └── clean.py
└── another-skill/
```

### 2. 双击运行

双击 `pack-skills.bat`，自动完成：

```
==================================================
SKILL PACKAGER
==================================================

[1/4] Scanning...
  Found 3 skill(s)

[2/4] Auditing...
  X skill-a: 0% (5 issue(s))
  ! skill-b: 55% (2 issue(s))
  V skill-c: 100% (0 issue(s))

[3/4] Fixing...
  skill-a: 6 fix(es) applied
  skill-b: 2 fix(es) applied
  skill-c: 0 fix(es) applied

[4/4] Testing...
  V skill-a: PASS
  V skill-b: PASS
  V skill-c: PASS

==================================================
RESULT: 3/3 skill(s) ready
Output: ready/
==================================================
```

### 3. 获取结果

标准化后的skills在 `ready/` 目录：

```
ready/
├── pdf-reader/
│   ├── SKILL.md
│   ├── LICENSE.txt
│   ├── requirements.txt
│   ├── scripts/
│   ├── references/
│   └── assets/
└── data-cleaner/
    └── ...
```

## 自动补全内容

| 检测到 | 自动生成 |
|--------|---------|
| Python代码 | `requirements.txt`（扫描import） |
| Node.js代码 | `package.json`（扫描require/import） |
| 缺SKILL.md | 从内容推断创建 |
| 缺frontmatter | 补全name/description |
| 缺LICENSE | 添加MIT许可 |
| 缺目录 | 创建scripts/references/assets |

## 审核检查项

| 检查项 | 问题处理 |
|--------|---------|
| SKILL.md存在 | 无则创建模板 |
| frontmatter完整 | 补全name/description |
| 依赖说明 | 检测代码自动生成 |
| LICENSE | 无则添加默认LICENSE |
| 目录结构 | 创建必要目录 |

## 分步命令（可选）

```bash
# 仅扫描
python scripts/scan.py incoming

# 仅审核
python scripts/audit.py incoming/skill-name

# 仅补全
python scripts/fix.py incoming ready

# 仅测试
python scripts/test.py ready/skill-name
```
