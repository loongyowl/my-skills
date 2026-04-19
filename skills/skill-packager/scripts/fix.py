#!/usr/bin/env python3
"""Fix missing files and standardize skill structure."""

import re
import shutil
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"


def fix_skill(skill_path: Path, output_path: Path) -> dict:
    if skill_path.is_file() and skill_path.suffix == ".md":
        return fix_single_md(skill_path, output_path)

    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a valid skill path")
        return {"fixed": False}

    skill_name = skill_path.name
    target = output_path / skill_name
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(skill_path, target)

    fixes = []

    fixes += fix_skill_md(target, skill_name)

    fixes += fix_license(target)

    fixes += fix_dependencies(target)

    fixes += fix_directory_structure(target)

    return {"name": skill_name, "path": str(target), "fixes": fixes}


def fix_single_md(md_path: Path, output_path: Path) -> dict:
    skill_name = md_path.stem
    fm = extract_frontmatter(md_path)
    if fm.get("name"):
        skill_name = fm["name"]

    target = output_path / skill_name
    target.mkdir(parents=True, exist_ok=True)

    fixes = []

    target_md = target / "SKILL.md"
    if md_path.name != "SKILL.md":
        shutil.copy2(md_path, target_md)
        fixes.append({"action": "renamed", "from": md_path.name, "to": "SKILL.md"})
    else:
        shutil.copy2(md_path, target_md)

    fixes += fix_skill_md(target, skill_name)
    fixes += fix_license(target)

    text = md_path.read_text(encoding="utf-8")
    if has_python_code(text):
        fixes += fix_dependencies(target)
    if has_js_code(text):
        fixes += fix_dependencies(target)

    fixes += fix_directory_structure(target)

    return {"name": skill_name, "path": str(target), "fixes": fixes}


def fix_skill_md(target: Path, skill_name: str) -> list[dict]:
    fixes = []
    skill_md = target / "SKILL.md"

    if not skill_md.exists():
        return fixes

    text = skill_md.read_text(encoding="utf-8")

    if not text.startswith("---"):
        desc = f"Use this skill when working with {skill_name}."
        fm = f"---\nname: {skill_name}\ndescription: \"{desc}\"\n---\n\n"
        text = fm + text
        skill_md.write_text(text, encoding="utf-8")
        fixes.append({"action": "added_frontmatter", "detail": "name and description"})
        return fixes

    end = text.find("---", 3)
    if end == -1:
        return fixes

    fm_text = text[3:end].strip()
    fm_lines = fm_text.splitlines()
    fm_dict = {}
    for line in fm_lines:
        if ":" in line:
            key, _, val = line.partition(":")
            fm_dict[key.strip()] = val.strip().strip('"').strip("'")

    modified = False

    if "name" not in fm_dict or not fm_dict["name"]:
        new_fm = f"name: {skill_name}"
        fm_text = new_fm + "\n" + fm_text
        modified = True
        fixes.append({"action": "added_field", "field": "name", "value": skill_name})

    if "description" not in fm_dict or not fm_dict["description"]:
        desc = f"Use this skill when working with {skill_name}."
        new_fm = f'description: "{desc}"'
        fm_text = fm_text + "\n" + new_fm
        modified = True
        fixes.append({"action": "added_field", "field": "description", "value": desc})

    if modified:
        text = "---\n" + fm_text + "\n---" + text[end + 3:]
        skill_md.write_text(text, encoding="utf-8")

    return fixes


def fix_license(target: Path) -> list[dict]:
    existing = [f for f in ["LICENSE", "LICENSE.txt", "LICENSE.md"] if (target / f).exists()]
    if existing:
        return []

    mit_template = ASSETS_DIR / "LICENSE_MIT.txt"
    if mit_template.exists():
        shutil.copy2(mit_template, target / "LICENSE.txt")
    else:
        default_license = """MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        (target / "LICENSE.txt").write_text(default_license, encoding="utf-8")

    return [{"action": "created", "file": "LICENSE.txt"}]


def fix_dependencies(target: Path) -> list[dict]:
    fixes = []
    py_files = list(target.rglob("*.py"))
    js_files = list(target.rglob("*.js")) + list(target.rglob("*.ts"))

    if py_files and not (target / "requirements.txt").exists():
        deps = scan_python_imports(py_files)
        if deps:
            (target / "requirements.txt").write_text("\n".join(sorted(deps)) + "\n", encoding="utf-8")
            fixes.append({"action": "created", "file": "requirements.txt", "dependencies": sorted(deps)})

    if js_files and not (target / "package.json").exists():
        deps = scan_js_imports(js_files, target.name)
        if deps.get("dependencies") or deps.get("devDependencies"):
            import json
            (target / "package.json").write_text(json.dumps(deps, indent=2) + "\n", encoding="utf-8")
            fixes.append({"action": "created", "file": "package.json"})

    return fixes


def scan_python_imports(py_files: list[Path]) -> list[str]:
    known_stdlib = {
        "os", "sys", "json", "re", "pathlib", "typing", "collections", "datetime",
        "io", "csv", "xml", "html", "http", "urllib", "hashlib", "shutil",
        "subprocess", "argparse", "logging", "tempfile", "copy", "math",
        "itertools", "functools", "operator", "textwrap", "dataclasses",
        "abc", "contextlib", "enum", "struct", "threading", "time",
    }
    known_map = {
        "openpyxl": "openpyxl",
        "PIL": "Pillow",
        "cv2": "opencv-python",
        "bs4": "beautifulsoup4",
        "sklearn": "scikit-learn",
        "yaml": "PyYAML",
        "docx": "python-docx",
        "pptx": "python-pptx",
        "magic": "python-magic",
        "gi": "PyGObject",
        "lxml": "lxml",
        "pandas": "pandas",
        "numpy": "numpy",
        "requests": "requests",
        "flask": "flask",
        "django": "django",
        "fastapi": "fastapi",
        "jinja2": "Jinja2",
        "markdown": "markdown",
        "pdfplumber": "pdfplumber",
        "fitz": "PyMuPDF",
        "reportlab": "reportlab",
        "boto3": "boto3",
        "redis": "redis",
        "celery": "celery",
    }

    imports = set()
    for py in py_files:
        try:
            text = py.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in re.finditer(r"^(?:from|import)\s+(\w+)", text, re.MULTILINE):
            pkg = m.group(1)
            if pkg in known_stdlib:
                continue
            if pkg in known_map:
                imports.add(known_map[pkg])
            elif pkg not in known_stdlib:
                imports.add(pkg)

    return list(imports)


def scan_js_imports(js_files: list[Path], skill_name: str) -> dict:
    known_node = {
        "fs", "path", "http", "https", "url", "util", "os", "crypto",
        "stream", "buffer", "events", "child_process", "net", "tls",
        "dns", "querystring", "assert", "zlib", "readline", "perf_hooks",
    }
    deps = {}
    for js in js_files:
        try:
            text = js.read_text(encoding="utf-8")
        except Exception:
            continue
        for m in re.finditer(r"(?:require\(['\"]|from\s+['\"])(@?[\w\-/]+)", text):
            pkg = m.group(1).split("/")[0] if m.group(1).startswith("@") else m.group(1).split("/")[0]
            if pkg not in known_node and not pkg.startswith(".") and pkg:
                deps[pkg] = "*"

    return {
        "name": skill_name,
        "version": "1.0.0",
        "dependencies": deps,
    }


def fix_directory_structure(target: Path) -> list[dict]:
    fixes = []
    for subdir in ["scripts", "references", "assets"]:
        d = target / subdir
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            (d / ".gitkeep").write_text("", encoding="utf-8")
            fixes.append({"action": "created_dir", "directory": subdir})
    return fixes


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


def has_python_code(text: str) -> bool:
    return bool(re.search(r"```python", text)) or bool(re.search(r"^import \w+|^from \w+", text, re.MULTILINE))


def has_js_code(text: str) -> bool:
    return bool(re.search(r"```(?:java)?script", text)) or bool(re.search(r"^(?:const|let|var|import|require)", text, re.MULTILINE))


def main():
    if len(sys.argv) < 3:
        print("Usage: python fix.py <incoming_dir> <output_dir>")
        sys.exit(1)

    incoming_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []

    if incoming_dir.is_file():
        result = fix_skill(incoming_dir, output_dir)
        results.append(result)
    elif incoming_dir.is_dir():
        items = sorted(incoming_dir.iterdir())
        for item in items:
            if item.name.startswith((".", "_")):
                continue
            if item.is_dir() or (item.is_file() and item.suffix == ".md"):
                result = fix_skill(item, output_dir)
                results.append(result)

    print(f"Fixed {len(results)} skill(s) → {output_dir}")
    print()
    for r in results:
        name = r.get("name", "unknown")
        fixes = r.get("fixes", [])
        print(f"  {name}: {len(fixes)} fix(es)")
        for f in fixes:
            action = f["action"]
            if "file" in f:
                print(f"    - {action}: {f['file']}")
            elif "field" in f:
                print(f"    - {action}: {f['field']}={f.get('value', '')}")
            elif "directory" in f:
                print(f"    - {action}: {f['directory']}/")
            elif "from" in f:
                print(f"    - {action}: {f['from']} -> {f.get('to', '')}")
            elif "detail" in f:
                print(f"    - {action}: {f['detail']}")
            else:
                print(f"    - {action}")

    return results


if __name__ == "__main__":
    main()
