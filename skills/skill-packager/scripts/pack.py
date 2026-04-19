#!/usr/bin/env python3
"""One-click pack: scan → audit → fix → test → report."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from scan import find_skills
from audit import audit_skill
from fix import fix_skill
from test import test_skill


def pack(incoming_dir: Path, output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 50)
    print("SKILL PACKAGER")
    print("=" * 50)
    print()

    print("[1/4] Scanning...")
    skills = find_skills(incoming_dir)
    print(f"  Found {len(skills)} skill(s)")
    print()

    print("[2/4] Auditing...")
    for s in skills:
        path = Path(s["path"])
        result = audit_skill(path)
        s["audit_score"] = result["score"]
        s["audit_issues"] = len(result["issues"])
        icon = "X" if result["score"] < 0.5 else "!" if result["score"] < 0.8 else "V"
        print(f"  {icon} {s['name']}: {result['score']:.0%} ({len(result['issues'])} issue(s))")
    print()

    print("[3/4] Fixing...")
    fix_results = []
    for s in skills:
        src = Path(s["path"])
        result = fix_skill(src, output_dir)
        fix_results.append(result)
        n = len(result.get("fixes", []))
        print(f"  {s['name']}: {n} fix(es) applied")
    print()

    print("[4/4] Testing...")
    test_results = []
    for fr in fix_results:
        target = Path(fr["path"])
        result = test_skill(target)
        test_results.append(result)
        icon = "V" if result["passed"] else "X"
        print(f"  {icon} {fr['name']}: {'PASS' if result['passed'] else 'FAIL'}")
        for err in result["errors"]:
            print(f"    - {err}")
    print()

    passed = sum(1 for r in test_results if r["passed"])
    total = len(test_results)

    print("=" * 50)
    print(f"RESULT: {passed}/{total} skill(s) ready")
    print(f"Output: {output_dir}")
    print("=" * 50)

    history = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "incoming": str(incoming_dir),
        "output": str(output_dir),
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "skills": [],
    }

    for i, s in enumerate(skills):
        history["skills"].append({
            "name": s["name"],
            "audit_score": s["audit_score"],
            "fixes_applied": len(fix_results[i].get("fixes", [])),
            "test_passed": test_results[i]["passed"],
            "test_errors": test_results[i]["errors"],
        })

    history_file = output_dir / "pack_history.json"
    existing = []
    if history_file.exists():
        try:
            existing = json.loads(history_file.read_text(encoding="utf-8"))
        except Exception:
            existing = []
    existing.append(history)
    history_file.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")

    return history


def main():
    if len(sys.argv) < 3:
        print("Usage: python pack.py <incoming_dir> <output_dir>")
        sys.exit(1)

    incoming_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    result = pack(incoming_dir, output_dir)

    if result["failed"] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
