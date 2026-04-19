#!/usr/bin/env python3
"""Scan incoming directory and discover skills."""

import json
import sys
from pathlib import Path


def find_skills(incoming_dir: Path) -> list[dict]:
    results = []
    if not incoming_dir.exists():
        print(f"Error: {incoming_dir} does not exist")
        return results

    for item in sorted(incoming_dir.iterdir()):
        if item.name.startswith((".", "_")):
            continue

        if item.is_dir():
            skill = scan_skill_dir(item)
            results.append(skill)
        elif item.is_file() and item.suffix == ".md":
            skill = scan_single_md(item)
            results.append(skill)

    return results


def scan_skill_dir(skill_dir: Path) -> dict:
    files = list(skill_dir.rglob("*"))
    file_count = sum(1 for f in files if f.is_file())
    file_names = [f.name for f in files if f.is_file()]

    has_skill_md = "SKILL.md" in file_names
    has_license = any(n.startswith("LICENSE") for n in file_names)
    has_requirements = "requirements.txt" in file_names
    has_package_json = "package.json" in file_names

    skill_name = skill_dir.name
    skill_md_path = skill_dir / "SKILL.md"
    frontmatter = extract_frontmatter(skill_md_path) if has_skill_md else {}

    return {
        "name": frontmatter.get("name", skill_name),
        "path": str(skill_dir),
        "type": "directory",
        "file_count": file_count,
        "files": file_names,
        "has_skill_md": has_skill_md,
        "has_license": has_license,
        "has_requirements": has_requirements,
        "has_package_json": has_package_json,
        "frontmatter": frontmatter,
    }


def scan_single_md(md_file: Path) -> dict:
    frontmatter = extract_frontmatter(md_file)
    skill_name = frontmatter.get("name", md_file.stem)

    return {
        "name": skill_name,
        "path": str(md_file),
        "type": "single_md",
        "file_count": 1,
        "files": [md_file.name],
        "has_skill_md": md_file.name == "SKILL.md",
        "has_license": False,
        "has_requirements": False,
        "has_package_json": False,
        "frontmatter": frontmatter,
    }


def extract_frontmatter(md_path: Path) -> dict:
    if not md_path.exists():
        return {}

    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return {}

    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    fm_text = text[3:end].strip()
    result = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            if val:
                result[key.strip()] = val

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python scan.py <incoming_dir>")
        sys.exit(1)

    incoming_dir = Path(sys.argv[1])
    skills = find_skills(incoming_dir)

    print(f"Found {len(skills)} skill(s) in {incoming_dir}")
    print()

    for s in skills:
        issues = []
        if not s["has_skill_md"]:
            issues.append("missing SKILL.md")
        if not s["has_license"]:
            issues.append("missing LICENSE")
        if not s["has_requirements"] and not s["has_package_json"]:
            issues.append("missing dependency file")
        if not s["frontmatter"].get("name"):
            issues.append("missing name in frontmatter")
        if not s["frontmatter"].get("description"):
            issues.append("missing description in frontmatter")

        status = "complete" if not issues else ", ".join(issues)
        print(f"  - {s['name']}: {s['file_count']} file(s), {status}")

    if len(sys.argv) > 2 and sys.argv[2] == "--json":
        print()
        print(json.dumps(skills, indent=2, ensure_ascii=False))

    return skills


if __name__ == "__main__":
    main()
