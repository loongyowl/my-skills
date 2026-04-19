import json
import hashlib
import time
import os
from pathlib import Path
from typing import Optional, Dict, List, Callable
from dataclasses import dataclass
from openai import OpenAI

from markdown_parser import MarkdownParser, split_into_chunks


@dataclass
class APIConfig:
    name: str
    base_url: str
    model: str
    api_key: str


@dataclass
class TranslationResult:
    success: bool
    content: str = ""
    error: str = ""


class Translator:
    def __init__(self, api_config: APIConfig):
        self.config = api_config
        self.client = OpenAI(
            base_url=api_config.base_url,
            api_key=api_config.api_key
        )
        self.parser = MarkdownParser()

    def translate_text(
        self,
        text: str,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ) -> TranslationResult:
        protected_text = self.parser.protect(text)

        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.config.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "你是一个专业的翻译助手，专门翻译哲学、心理学、宗教等领域的人文书籍。请将用户提供的文本翻译成中文，保持原文的学术性和准确性。只输出翻译结果，不要添加任何解释或注释。"
                        },
                        {"role": "user", "content": protected_text}
                    ],
                    timeout=30
                )
                translated = response.choices[0].message.content
                restored = self.parser.restore(translated)
                return TranslationResult(success=True, content=restored)

            except Exception as e:
                if attempt < max_retries - 1:
                    delay = retry_delay * (2 ** attempt)
                    time.sleep(delay)
                else:
                    return TranslationResult(
                        success=False,
                        error=str(e)
                    )

        return TranslationResult(success=False, error="Max retries exceeded")

    def translate_file(
        self,
        file_path: Path,
        output_path: Path,
        manifest: Dict,
        max_chars_per_chunk: int = 3000,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> TranslationResult:
        file_hash = self._get_file_hash(file_path)

        if manifest.get("files", {}).get(str(file_path), {}).get("source_hash") == file_hash:
            if manifest["files"][str(file_path)].get("translated"):
                return TranslationResult(success=True, content="")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, "r", encoding="utf-8-sig") as f:
                    content = f.read()
            except Exception as e:
                return TranslationResult(success=False, error=f"Encoding error: {e}")
        except Exception as e:
            return TranslationResult(success=False, error=f"Read error: {e}")

        if not content.strip():
            return TranslationResult(success=False, error="Empty file")

        chunks = split_into_chunks(content, max_chars_per_chunk)
        translated_chunks: List[str] = []
        total_chunks = len(chunks)

        for i, chunk in enumerate(chunks):
            if progress_callback:
                progress_callback(i + 1, total_chunks)

            result = self.translate_text(chunk)
            if not result.success:
                return TranslationResult(
                    success=False,
                    error=f"Chunk {i+1} failed: {result.error}"
                )
            translated_chunks.append(result.content)

        final_content = "\n\n".join(translated_chunks)

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(final_content)
        except Exception as e:
            return TranslationResult(success=False, error=f"Write error: {e}")

        return TranslationResult(success=True, content=final_content)

    def _get_file_hash(self, file_path: Path) -> str:
        with open(file_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()


class ManifestManager:
    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path
        self.manifest: Dict = {}
        self._load()

    def _load(self):
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, "r", encoding="utf-8") as f:
                    self.manifest = json.load(f)
            except Exception:
                self.manifest = {"files": {}}
        else:
            self.manifest = {"files": {}}

    def save(self):
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.manifest, f, indent=2, ensure_ascii=False)

    def mark_translated(self, file_path: Path, source_hash: str):
        self.manifest["files"][str(file_path)] = {
            "source_hash": source_hash,
            "translated": True,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        self.save()

    def is_translated(self, file_path: Path, current_hash: str) -> bool:
        entry = self.manifest["files"].get(str(file_path))
        return entry and entry.get("translated") and entry.get("source_hash") == current_hash

    def get_pending_files(self, files: List[Path]) -> List[Path]:
        pending = []
        for f in files:
            hash_val = hashlib.sha256(open(f, "rb").read()).hexdigest()
            if not self.is_translated(f, hash_val):
                pending.append(f)
        return pending


DEFAULT_APIS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat"
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o"
    },
    "custom": {
        "base_url": "",
        "model": ""
    }
}