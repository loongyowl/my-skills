import os
import json
import re
from datetime import datetime
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"
INDEX_FILE = Path(__file__).parent / "index.json"
README_FILE = Path(__file__).parent / "README.md"


def parse_skill_md(skill_path: Path) -> dict:
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None

    content = skill_file.read_text(encoding="utf-8")

    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        return None

    frontmatter = frontmatter_match.group(1)
    data = {}

    for line in frontmatter.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            data[key] = value

    return data


def scan_skills() -> dict:
    skills = {}

    if not SKILLS_DIR.exists():
        return skills

    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            skill_info = parse_skill_md(item)
            if skill_info and "name" in skill_info:
                skill_name = skill_info["name"]
                skills[skill_name] = {
                    "name": skill_name,
                    "description": skill_info.get("description", ""),
                    "tags": skill_info.get("tags", "").split(",") if skill_info.get("tags") else [],
                    "license": skill_info.get("license", "Unknown"),
                    "path": f"skills/{item.name}"
                }

    return skills


def generate_index(skills: dict) -> dict:
    return {
        "version": "1.0.0",
        "updated": datetime.now().isoformat(),
        "skills": skills
    }


def generate_readme(skills: dict) -> str:
    lines = [
        "# Skills Repository",
        "",
        f"Last updated: {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Available Skills",
        "",
        "| Skill | Description | License |",
        "|-------|-------------|---------|",
    ]

    for name, info in sorted(skills.items()):
        desc = info.get("description", "")[:80]
        if len(info.get("description", "")) > 80:
            desc += "..."
        license = info.get("license", "Unknown")
        lines.append(f"| {name} | {desc} | {license} |")

    lines.append("")
    lines.append("## Installation")
    lines.append("")
    lines.append("Use the CLI tool to search and install skills:")
    lines.append("```bash")
    lines.append("# Search for a skill")
    lines.append("skills-cli search <keyword>")
    lines.append("")
    lines.append("# Install a skill")
    lines.append("skills-cli install <skill-name>")
    lines.append("```")

    return "\n".join(lines)


def main():
    print("Scanning skills...")
    skills = scan_skills()

    print(f"Found {len(skills)} skills")

    index_data = generate_index(skills)
    INDEX_FILE.write_text(json.dumps(index_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Updated index.json")

    readme_content = generate_readme(skills)
    README_FILE.write_text(readme_content, encoding="utf-8")
    print(f"Updated README.md")

    print("Done!")


if __name__ == "__main__":
    main()
