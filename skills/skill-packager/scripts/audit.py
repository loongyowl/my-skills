#!/usr/bin/env python3
"""Audit a skill for completeness and standard compliance."""

import json
import sys
from pathlib import Path


def audit_skill(skill_path: Path) -> dict:
    result = {
        "path": str(skill_path),
        "name": "",
        "checks": {},
        "issues": [],
        "score": 0.0,
    }

    if skill_path.is_file() and skill_path.suffix == ".md":
        return audit_single_md(skill_path, result)

    if not skill_path.is_dir():
        result["issues"].append({"level": "critical", "check": "path", "message": f"Not a valid path: {skill_path}"})
        return result

    skill_name = skill_path.name
    result["name"] = skill_name

    skill_md = skill_path / "SKILL.md"
    check_skill_md(skill_md, result)

    check_license(skill_path, result)

    check_dependencies(skill_path, result)

    check_directory_structure(skill_path, result)

    total = len(result["checks"])
    passed = sum(1 for v in result["checks"].values() if v)
    result["score"] = round(passed / total, 2) if total > 0 else 0.0

    return result


def audit_single_md(md_path: Path, result: dict) -> dict:
    result["name"] = md_path.stem
    result["checks"]["has_skill_md"] = False
    result["checks"]["has_frontmatter"] = False
    result["checks"]["has_name"] = False
    result["checks"]["has_description"] = False
    result["checks"]["has_license"] = False
    result["checks"]["has_dependencies"] = False

    result["issues"].append({"level": "critical", "check": "has_skill_md", "message": "Single md file, not a proper skill directory"})
    result["issues"].append({"level": "warning", "check": "has_license", "message": "Missing LICENSE file"})
    result["issues"].append({"level": "warning", "check": "has_dependencies", "message": "Missing dependency file"})

    if md_path.name != "SKILL.md":
        result["issues"].append({"level": "critical", "check": "has_skill_md", "message": f"File is named '{md_path.name}', should be 'SKILL.md'"})

    fm = extract_frontmatter(md_path)
    if fm:
        result["checks"]["has_frontmatter"] = True
        if fm.get("name"):
            result["checks"]["has_name"] = True
            result["name"] = fm["name"]
        else:
            result["issues"].append({"level": "critical", "check": "has_name", "message": "Missing 'name' in frontmatter"})
        if fm.get("description"):
            result["checks"]["has_description"] = True
        else:
            result["issues"].append({"level": "critical", "check": "has_description", "message": "Missing 'description' in frontmatter"})
    else:
        result["issues"].append({"level": "critical", "check": "has_frontmatter", "message": "Missing YAML frontmatter"})

    total = len(result["checks"])
    passed = sum(1 for v in result["checks"].values() if v)
    result["score"] = round(passed / total, 2) if total > 0 else 0.0

    return result


def check_skill_md(skill_md: Path, result: dict):
    if skill_md.exists():
        result["checks"]["has_skill_md"] = True
        fm = extract_frontmatter(skill_md)
        if fm:
            result["checks"]["has_frontmatter"] = True
            if fm.get("name"):
                result["checks"]["has_name"] = True
                result["name"] = fm["name"]
            else:
                result["checks"]["has_name"] = False
                result["issues"].append({"level": "critical", "check": "has_name", "message": "Missing 'name' in frontmatter"})
            if fm.get("description"):
                result["checks"]["has_description"] = True
            else:
                result["checks"]["has_description"] = False
                result["issues"].append({"level": "critical", "check": "has_description", "message": "Missing 'description' in frontmatter"})
        else:
            result["checks"]["has_frontmatter"] = False
            result["checks"]["has_name"] = False
            result["checks"]["has_description"] = False
            result["issues"].append({"level": "critical", "check": "has_frontmatter", "message": "SKILL.md missing YAML frontmatter"})
    else:
        result["checks"]["has_skill_md"] = False
        result["checks"]["has_frontmatter"] = False
        result["checks"]["has_name"] = False
        result["checks"]["has_description"] = False
        result["issues"].append({"level": "critical", "check": "has_skill_md", "message": "Missing SKILL.md"})


def check_license(skill_path: Path, result: dict):
    has_license = any((skill_path / f).exists() for f in ["LICENSE", "LICENSE.txt", "LICENSE.md"])
    result["checks"]["has_license"] = has_license
    if not has_license:
        result["issues"].append({"level": "warning", "check": "has_license", "message": "Missing LICENSE file"})


def check_dependencies(skill_path: Path, result: dict):
    py_files = list(skill_path.rglob("*.py"))
    js_files = list(skill_path.rglob("*.js")) + list(skill_path.rglob("*.ts"))

    has_req = (skill_path / "requirements.txt").exists()
    has_pkg = (skill_path / "package.json").exists()

    needs_py = len(py_files) > 0
    needs_js = len(js_files) > 0

    if needs_py:
        result["checks"]["has_python_deps"] = has_req
        if not has_req:
            result["issues"].append({"level": "warning", "check": "has_python_deps", "message": f"Python files found but no requirements.txt"})
    else:
        result["checks"]["has_python_deps"] = True

    if needs_js:
        result["checks"]["has_js_deps"] = has_pkg
        if not has_pkg:
            result["issues"].append({"level": "warning", "check": "has_js_deps", "message": f"JS/TS files found but no package.json"})
    else:
        result["checks"]["has_js_deps"] = True

    result["checks"]["has_dependencies"] = result["checks"]["has_python_deps"] and result["checks"]["has_js_deps"]


def check_directory_structure(skill_path: Path, result: dict):
    has_scripts = (skill_path / "scripts").is_dir()
    has_refs = (skill_path / "references").is_dir()
    has_assets = (skill_path / "assets").is_dir()

    result["checks"]["has_scripts_dir"] = has_scripts
    result["checks"]["has_references_dir"] = has_refs
    result["checks"]["has_assets_dir"] = has_assets

    if not has_scripts:
        result["issues"].append({"level": "info", "check": "has_scripts_dir", "message": "No scripts/ directory"})
    if not has_refs:
        result["issues"].append({"level": "info", "check": "has_references_dir", "message": "No references/ directory"})
    if not has_assets:
        result["issues"].append({"level": "info", "check": "has_assets_dir", "message": "No assets/ directory"})


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
        print("Usage: python audit.py <skill_path>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    result = audit_skill(skill_path)

    level_order = {"critical": 0, "warning": 1, "info": 2}
    level_icon = {"critical": "X", "warning": "!", "info": "i"}

    print(f"Audit: {result['name']}")
    print(f"Score: {result['score']:.0%}")
    print()

    if result["issues"]:
        sorted_issues = sorted(result["issues"], key=lambda x: level_order.get(x["level"], 9))
        for issue in sorted_issues:
            icon = level_icon.get(issue["level"], "?")
            print(f"  {icon} [{issue['level']}] {issue['message']}")
    else:
        print("  All checks passed!")

    if len(sys.argv) > 2 and sys.argv[2] == "--json":
        print()
        print(json.dumps(result, indent=2, ensure_ascii=False))

    return result


if __name__ == "__main__":
    main()
