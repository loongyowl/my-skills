import sys
sys.path.insert(0, str(__file__).rpartition("\\")[0])

from markdown_parser import MarkdownParser, split_into_chunks

def test_parser():
    parser = MarkdownParser()

    test_cases = [
        ("## Title", "## "),
        ("**bold text**", "**"),
        ("*italic*", "*"),
        ("`inline code`", "`"),
        ("[link](url)", "]("),
        ("![image](url)", "]("),
        ("$math$", "$"),
        ("$$block math$$", "$$"),
        ("[^footnote]", "[^"),
    ]

    print("=== Test: Format Protection ===")
    for text, marker in test_cases:
        protected = parser.protect(text)
        restored = parser.restore(protected)
        ok = "OK" if marker in restored else "FAIL"
        print(f"[{ok}] {text} | {protected[:30]}... | {restored}")

    print("\n=== Test: Code Block ===")
    code_block = """```python
def hello():
    print("world")
```"""
    protected = parser.protect(code_block)
    restored = parser.restore(protected)
    print(f"Original:\n{code_block}")
    print(f"\nProtected:\n{protected}")
    print(f"\nRestored:\n{restored}")
    print(f"Match: {'OK' if code_block == restored else 'FAIL'}")

    print("\n=== Test: Complex Markdown ===")
    complex_md = """
## Chapter 1: Wisdom

> Philosophy begins with **wonder**.

The *greatest* wisdom is to know that you know nothing. `Socrates` said:

> Know thyself.

See [Stanford Encyclopedia](https://plato.stanford.edu) for more.

```python
def wisdom():
    return "knowledge"
```

Math: $E = mc^2$
"""
    protected = parser.protect(complex_md)
    restored = parser.restore(protected)
    print(f"Original length: {len(complex_md)}")
    print(f"Contains placeholders: {'___' in protected}")
    print(f"Restored matches original: {'OK' if complex_md == restored else 'FAIL'}")

    print("\n=== Test: Chunk Splitting ===")
    long_text = "\n".join([f"Line {i}: " + "x" * 100 for i in range(50)])
    chunks = split_into_chunks(long_text, max_chars=500)
    print(f"Total chars: {len(long_text)}")
    print(f"Chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):
        print(f"  Chunk {i+1}: {len(chunk)} chars")
    print(f"  ...")
    print(f"All chunks total: {sum(len(c) for c in chunks)} chars")

if __name__ == "__main__":
    test_parser()
