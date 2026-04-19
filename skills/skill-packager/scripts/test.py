#!/usr/bin/env python3
"""Test whether a skill is usable after packaging."""

import json
import sys
from pathlib import Path


def test_skill(skill_path: Path) -> dict:
    result = {
        "path": str(skill_path),
        "name": "",
        "tests": {},
        "passed": True,
        "errors": [],
    }

    if not skill_path.exists():
        result["tests"]["exists"] = False
        result["passed"] = False
        result["errors"].append(f"Path does not exist: {skill_path}")
        return result

    if skill_path.is_file() and skill_path.suffix == ".md":
        result["tests"]["is_skill_dir"] = False
        result["passed"] = False
        result["errors"].append("Not a skill directory (single md file)")
        return result

    skill_name = skill_path.name
    result["name"] = skill_name

    test_skill_md(skill_path, result)
    test_frontmatter(skill_path, result)
    test_license(skill_path, result)
    test_dependencies(skill_path, result)
    test_scripts(skill_path, result)

    result["passed"] = all(v for v in result["tests"].values())

    return result


def test_skill_md(skill_path: Path, result: dict):
    skill_md = skill_path / "SKILL.md"
    exists = skill_md.exists()
    result["tests"]["skill_md_exists"] = exists

    if not exists:
        result["errors"].append("SKILL.md not found")
        return

    try:
        text = skill_md.read_text(encoding="utf-8")
        if not text.strip():
            result["tests"]["skill_md_not_empty"] = False
            result["errors"].append("SKILL.md is empty")
        else:
            result["tests"]["skill_md_not_empty"] = True
    except Exception as e:
        result["tests"]["skill_md_not_empty"] = False
        result["errors"].append(f"Cannot read SKILL.md: {e}")


def test_frontmatter(skill_path: Path, result: dict):
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result["tests"]["frontmatter_valid"] = False
        result["tests"]["frontmatter_has_name"] = False
        result["tests"]["frontmatter_has_description"] = False
        return

    try:
        text = skill_md.read_text(encoding="utf-8")
    except Exception:
        result["tests"]["frontmatter_valid"] = False
        result["tests"]["frontmatter_has_name"] = False
        result["tests"]["frontmatter_has_description"] = False
        return

    if not text.startswith("---"):
        result["tests"]["frontmatter_valid"] = False
        result["tests"]["frontmatter_has_name"] = False
        result["tests"]["frontmatter_has_description"] = False
        result["errors"].append("SKILL.md missing YAML frontmatter (---)")
        return

    end = text.find("---", 3)
    if end == -1:
        result["tests"]["frontmatter_valid"] = False
        result["tests"]["frontmatter_has_name"] = False
        result["tests"]["frontmatter_has_description"] = False
        result["errors"].append("SKILL.md frontmatter not properly closed")
        return

    result["tests"]["frontmatter_valid"] = True

    fm_text = text[3:end].strip()
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            val = val.strip().strip('"').strip("'")
            if val:
                fm[key.strip()] = val

    has_name = "name" in fm and len(fm["name"]) > 0
    result["tests"]["frontmatter_has_name"] = has_name
    if has_name:
        result["name"] = fm["name"]
    else:
        result["errors"].append("frontmatter missing 'name'")

    has_desc = "description" in fm and len(fm["description"]) > 10
    result["tests"]["frontmatter_has_description"] = has_desc
    if not has_desc:
        result["errors"].append("frontmatter missing or too short 'description'")


def test_license(skill_path: Path, result: dict):
    has_license = any((skill_path / f).exists() for f in ["LICENSE", "LICENSE.txt", "LICENSE.md"])
    result["tests"]["has_license"] = has_license
    if not has_license:
        result["errors"].append("No LICENSE file found")


def test_dependencies(skill_path: Path, result: dict):
    py_files = list(skill_path.rglob("*.py"))
    js_files = list(skill_path.rglob("*.js")) + list(skill_path.rglob("*.ts"))

    if py_files:
        has_req = (skill_path / "requirements.txt").exists()
        result["tests"]["python_deps"] = has_req
        if not has_req:
            result["errors"].append("Python files found but no requirements.txt")
    else:
        result["tests"]["python_deps"] = True

    if js_files:
        has_pkg = (skill_path / "package.json").exists()
        result["tests"]["js_deps"] = has_pkg
        if not has_pkg:
            result["errors"].append("JS/TS files found but no package.json")
    else:
        result["tests"]["js_deps"] = True


def test_scripts(skill_path: Path, result: dict):
    scripts_dir = skill_path / "scripts"
    if not scripts_dir.exists():
        result["tests"]["scripts_runnable"] = True
        return

    py_scripts = list(scripts_dir.glob("*.py"))
    if not py_scripts:
        result["tests"]["scripts_runnable"] = True
        return

    import subprocess

    all_ok = True
    for script in py_scripts:
        try:
            r = subprocess.run(
                [sys.executable, "-c", f"import ast; ast.parse(open(r'{script}').read())"],
                capture_output=True, text=True, timeout=10,
            )
            if r.returncode != 0:
                all_ok = False
                result["errors"].append(f"Syntax error in {script.name}: {r.stderr.strip()[:100]}")
        except Exception as e:
            all_ok = False
            result["errors"].append(f"Cannot check {script.name}: {e}")

    result["tests"]["scripts_runnable"] = all_ok


def main():
    if len(sys.argv) < 2:
        print("Usage: python test.py <skill_path> [skill_path2 ...]")
        sys.exit(1)

    all_results = []

    for path_str in sys.argv[1:]:
        skill_path = Path(path_str)
        result = test_skill(skill_path)
        all_results.append(result)

        icon = "V" if result["passed"] else "X"
        print(f"{icon} {result['name']}: {'PASS' if result['passed'] else 'FAIL'}")
        if result["errors"]:
            for err in result["errors"]:
                print(f"  - {err}")

    passed = sum(1 for r in all_results if r["passed"])
    total = len(all_results)
    print(f"\n{passed}/{total} skill(s) passed")

    if "--json" in sys.argv:
        print(json.dumps(all_results, indent=2, ensure_ascii=False))

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
