import re
from typing import List, Tuple, Dict


class MarkdownParser:
    def __init__(self):
        self.placeholders: Dict[str, str] = {}
        self._counter = 0

    def _next_id(self, prefix: str) -> str:
        self._counter += 1
        return f"___{prefix}_{self._counter}___"

    def protect(self, text: str) -> str:
        self.placeholders.clear()
        self._counter = 0

        text = self._protect_fenced_code(text)
        text = self._protect_inline_code(text)
        text = self._protect_math_blocks(text)
        text = self._protect_inline_math(text)
        text = self._protect_links_images(text)
        text = self._protect_footnotes(text)
        text = self._protect_bold_italic(text)
        return text

    def restore(self, text: str) -> str:
        for placeholder, original in sorted(
            self.placeholders.items(), key=lambda x: len(x[0]), reverse=True
        ):
            text = text.replace(placeholder, original)
        return text

    def _protect_fenced_code(self, text: str) -> str:
        pattern = re.compile(r"(```[\s\S]*?```|~~~[\s\S]*?~~~)", re.MULTILINE)
        return pattern.sub(self._make_replacer("CODE_BLOCK"), text)

    def _protect_inline_code(self, text: str) -> str:
        pattern = re.compile(r"`([^`\n]+)`")
        return pattern.sub(self._make_replacer("CODE_INLINE"), text)

    def _protect_math_blocks(self, text: str) -> str:
        pattern = re.compile(r"\$\$[\s\S]*?\$\$", re.MULTILINE)
        return pattern.sub(self._make_replacer("MATH_BLOCK"), text)

    def _protect_inline_math(self, text: str) -> str:
        pattern = re.compile(r"(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)")
        return pattern.sub(self._make_replacer("MATH_INLINE"), text)

    def _protect_links_images(self, text: str) -> str:
        pattern = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
        text = pattern.sub(self._make_replacer("IMG"), text)
        pattern = re.compile(r"(?<!\!)\[([^\]]*)\]\([^)]+\)")
        text = pattern.sub(self._make_replacer("LINK"), text)
        return text

    def _protect_footnotes(self, text: str) -> str:
        pattern = re.compile(r"\[\^[^\]]+\]")
        return pattern.sub(self._make_replacer("FOOTNOTE"), text)

    def _protect_bold_italic(self, text: str) -> str:
        pattern = re.compile(r"\*\*\*(.+?)\*\*\*")
        text = pattern.sub(self._make_replacer("BOLD_ITALIC"), text)
        pattern = re.compile(r"\*\*(.+?)\*\*")
        text = pattern.sub(self._make_replacer("BOLD"), text)
        pattern = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
        text = pattern.sub(self._make_replacer("ITALIC"), text)
        return text

    def _make_replacer(self, prefix: str):
        def replacer(match: re.Match) -> str:
            placeholder = self._next_id(prefix)
            self.placeholders[placeholder] = match.group(0)
            return placeholder
        return replacer


def split_into_chunks(text: str, max_chars: int = 3000) -> List[str]:
    if len(text) <= max_chars:
        return [text] if text.strip() else []

    chunks: List[str] = []
    lines = text.split("\n")
    current_chunk: List[str] = []
    current_len = 0
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block

        line_len = len(line) + 1

        if current_len + line_len > max_chars and current_chunk and not in_code_block:
            chunk_text = "\n".join(current_chunk)
            if chunk_text.strip():
                chunks.append(chunk_text)
            current_chunk = [line]
            current_len = line_len
        else:
            current_chunk.append(line)
            current_len += line_len

    if current_chunk:
        chunk_text = "\n".join(current_chunk)
        if chunk_text.strip():
            chunks.append(chunk_text)

    return chunks
