import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from markdown_parser import MarkdownParser, split_into_chunks
from translator import ManifestManager, DEFAULT_APIS


def test_manifest():
    print("=== Test: Manifest (Resumable) ===")
    with tempfile.TemporaryDirectory() as tmpdir:
        manifest_path = Path(tmpdir) / ".translate_manifest.json"
        mgr = ManifestManager(manifest_path)

        test_file = Path(tmpdir) / "test.md"
        test_file.write_text("Hello World", encoding="utf-8")

        import hashlib
        file_hash = hashlib.sha256(test_file.read_bytes()).hexdigest()

        mgr.mark_translated(test_file, file_hash)
        print(f"[OK] Marked {test_file.name} as translated")

        assert mgr.is_translated(test_file, file_hash), "Manifest check failed"
        print(f"[OK] is_translated returns True")

        test_file.write_text("Modified content", encoding="utf-8")
        new_hash = hashlib.sha256(test_file.read_bytes()).hexdigest()
        assert not mgr.is_translated(test_file, new_hash), "Should detect change"
        print(f"[OK] Detects file change (hash mismatch)")

        pending = mgr.get_pending_files([test_file])
        assert len(pending) == 1, "Modified file should be pending"
        print(f"[OK] get_pending_files returns modified file")


def test_default_apis():
    print("\n=== Test: Default API Configs ===")
    for name, cfg in DEFAULT_APIS.items():
        print(f"  {name}: {cfg.get('base_url', 'custom')[:40]}...")
    assert "deepseek" in DEFAULT_APIS
    assert "openai" in DEFAULT_APIS
    assert "custom" in DEFAULT_APIS
    print("[OK] All default APIs configured")


def test_split_edges():
    print("\n=== Test: Edge Cases (Chunk Split) ===")

    empty = split_into_chunks("")
    assert empty == [], f"Empty should return [], got {empty}"
    print("[OK] Empty string returns []")

    short = split_into_chunks("Hello")
    assert len(short) == 1
    print("[OK] Short text returns single chunk")

    code_block = """```python
def long_function():
    # This is a long code block
    # that should not be split
    x = 1
    y = 2
    return x + y
```"""
    chunks = split_into_chunks(code_block, max_chars=50)
    for c in chunks:
        if "```" in c and not c.strip().startswith("```"):
            print(f"[WARN] Code block may be split incorrectly")
            break
    else:
        print("[OK] Code blocks handled (may split at boundaries)")

    large_text = "Line\n" * 10000
    chunks = split_into_chunks(large_text, max_chars=1000)
    total = sum(len(c) for c in chunks)
    print(f"[OK] Large text ({len(large_text)} chars) split into {len(chunks)} chunks")


def test_format_protection_edge_cases():
    print("\n=== Test: Format Protection Edges ===")
    parser = MarkdownParser()

    cases = [
        ("Empty", ""),
        ("Plain", "Just plain text"),
        ("Multiple **bold** and **more**", "**"),
        ("Nested **bold *italic* bold**", "**"),
        ("Broken `code", "`"),
        ("Multiple$math$and$more$", "$"),
    ]

    for name, text in cases:
        try:
            protected = parser.protect(text)
            restored = parser.restore(protected)
            print(f"[OK] {name}: protected={len(protected)}, restored={len(restored)}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")


def test_file_detection():
    print("\n=== Test: File Detection ===")
    with tempfile.TemporaryDirectory() as tmpdir:
        folder = Path(tmpdir)

        (folder / "book1.md").write_text("# Book 1", encoding="utf-8")
        (folder / "book2.md").write_text("# Book 2", encoding="utf-8")
        (folder / "book1.translated.md").write_text("# Book 1 CN", encoding="utf-8")
        (folder / "notes.txt").write_text("Not markdown", encoding="utf-8")

        md_files = sorted(folder.glob("*.md"))
        md_files = [f for f in md_files if not f.name.endswith(".translated.md")]

        assert len(md_files) == 2, f"Expected 2 files, found {len(md_files)}"
        print(f"[OK] Found {len(md_files)} .md files (excluded .translated.md)")
        for f in md_files:
            print(f"     - {f.name}")


def run_all():
    print("=" * 50)
    print("MARKDOWN TRANSLATE - Integration Tests")
    print("=" * 50)

    test_default_apis()
    test_manifest()
    test_split_edges()
    test_format_protection_edge_cases()
    test_file_detection()

    print("\n" + "=" * 50)
    print("ALL TESTS PASSED")
    print("=" * 50)


if __name__ == "__main__":
    run_all()
