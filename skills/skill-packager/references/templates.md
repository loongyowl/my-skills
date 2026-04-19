# Skill Templates

## Standard Skill Directory Structure

```
skill-name/
├── SKILL.md           # Required: skill definition with frontmatter
├── LICENSE.txt        # Recommended: license file
├── requirements.txt   # If Python scripts present
├── package.json       # If Node.js scripts present
├── scripts/           # Executable code
│   └── *.py or *.js
├── references/        # Documentation loaded as needed
│   └── *.md
├── assets/            # Files used in output (templates, fonts)
│   └── *
└── examples/          # Example usage (optional)
    └── *
```

## SKILL.md Template

```markdown
---
name: skill-name
description: "When to trigger and what the skill does. Be specific about contexts. Use pushy style - trigger whenever related keywords appear even if not explicitly named."
license: MIT  # or "Proprietary. LICENSE.txt has complete terms"
---

# Skill Title

Brief overview of what this skill enables.

## When to Use

Describe specific scenarios and trigger contexts.

## Usage

### Basic Usage

```bash
python scripts/main.py <args>
```

### Options

| Option | Description |
|--------|-------------|
| --foo  | Does foo |

## Output Format

Describe expected output structure.

## Examples

**Example 1:**
Input: ...
Output: ...

## Notes

Any additional notes or best practices.
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier, lowercase with hyphens |
| `description` | Yes | Trigger description, 50-200 chars, pushy style |
| `license` | No | License type (MIT, Proprietary, etc.) |
| `version` | No | Skill version |
| `compatibility` | No | Required tools/dependencies |

## Description Guidelines (Pushy Style)

Bad: "A skill for working with PDF files."

Good: "Use this skill when working with PDF files - reading, extracting text, converting formats, or manipulating pages. Trigger whenever the user mentions PDF, pdf, PDFs, or asks to extract/read/convert document content, even if they don't explicitly say 'PDF skill'."

## requirements.txt Template

```
# Dependencies for skill-name
openpyxl>=3.0.0
pandas>=2.0.0
```

## package.json Template

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "dependencies": {
    "docx": "^1.0.0"
  }
}
```

## LICENSE.txt Template (MIT)

See `assets/LICENSE_MIT.txt`.