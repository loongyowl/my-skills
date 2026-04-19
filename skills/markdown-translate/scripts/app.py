import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import json
import os
import sys
from pathlib import Path
from typing import Optional

from translator import Translator, APIConfig, ManifestManager, DEFAULT_APIS

CONFIG_FILE = Path(__file__).parent / "config.json"


class TranslateApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Markdown 批量翻译工具")
        self.root.geometry("720x680")
        self.root.resizable(True, True)

        self.is_running = False
        self.is_paused = False
        self.should_stop = False
        self.config = self._load_config()
        self.translator: Optional[Translator] = None

        self._build_ui()
        self._load_api_fields()
        self._on_mode_change()

    def _load_config(self) -> dict:
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        cfg = {"apis": {}, "last_used": "deepseek"}
        for name, vals in DEFAULT_APIS.items():
            cfg["apis"][name] = {**vals, "api_key": ""}
        return cfg

    def _save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill=tk.BOTH, expand=True)

        api_frame = ttk.LabelFrame(main, text="API 配置", padding=8)
        api_frame.pack(fill=tk.X, pady=(0, 8))

        row0 = ttk.Frame(api_frame)
        row0.pack(fill=tk.X, pady=2)
        ttk.Label(row0, text="选择 API:").pack(side=tk.LEFT)
        self.api_var = tk.StringVar(value=self.config.get("last_used", "deepseek"))
        self.api_combo = ttk.Combobox(
            row0, textvariable=self.api_var,
            values=list(DEFAULT_APIS.keys()), state="readonly", width=12
        )
        self.api_combo.pack(side=tk.LEFT, padx=8)
        self.api_combo.bind("<<ComboboxSelected>>", self._on_api_change)

        row1 = ttk.Frame(api_frame)
        row1.pack(fill=tk.X, pady=2)
        ttk.Label(row1, text="API Key:").pack(side=tk.LEFT)
        self.key_var = tk.StringVar()
        self.key_entry = ttk.Entry(row1, textvariable=self.key_var, width=52, show="*")
        self.key_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)
        self.show_key_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(row1, text="显示", variable=self.show_key_var,
                        command=self._toggle_key).pack(side=tk.LEFT)

        row2 = ttk.Frame(api_frame)
        row2.pack(fill=tk.X, pady=2)
        ttk.Label(row2, text="Base URL:").pack(side=tk.LEFT)
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(row2, textvariable=self.url_var, width=52)
        self.url_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)

        row3 = ttk.Frame(api_frame)
        row3.pack(fill=tk.X, pady=2)
        ttk.Label(row3, text="Model:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar()
        self.model_entry = ttk.Entry(row3, textvariable=self.model_var, width=30)
        self.model_entry.pack(side=tk.LEFT, padx=8)

        dir_frame = ttk.LabelFrame(main, text="文件选择", padding=8)
        dir_frame.pack(fill=tk.X, pady=(0, 8))

        row_mode = ttk.Frame(dir_frame)
        row_mode.pack(fill=tk.X, pady=2)
        self.mode_var = tk.StringVar(value="folder")
        ttk.Radiobutton(row_mode, text="单个文件", variable=self.mode_var,
                        value="file", command=self._on_mode_change).pack(side=tk.LEFT, padx=8)
        ttk.Radiobutton(row_mode, text="文件夹(批量)", variable=self.mode_var,
                        value="folder", command=self._on_mode_change).pack(side=tk.LEFT, padx=8)

        row_file = ttk.Frame(dir_frame)
        row_file.pack(fill=tk.X, pady=2)
        ttk.Label(row_file, text="选择文件:").pack(side=tk.LEFT)
        self.file_var = tk.StringVar()
        self.file_entry = ttk.Entry(row_file, textvariable=self.file_var, width=48)
        self.file_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)
        self.file_btn = ttk.Button(row_file, text="浏览...", command=self._browse_file)
        self.file_btn.pack(side=tk.LEFT)

        row_dir = ttk.Frame(dir_frame)
        row_dir.pack(fill=tk.X, pady=2)
        ttk.Label(row_dir, text="选择文件夹:").pack(side=tk.LEFT)
        self.dir_var = tk.StringVar()
        self.dir_entry = ttk.Entry(row_dir, textvariable=self.dir_var, width=48)
        self.dir_entry.pack(side=tk.LEFT, padx=8, fill=tk.X, expand=True)
        self.dir_btn = ttk.Button(row_dir, text="浏览...", command=self._browse_dir)
        self.dir_btn.pack(side=tk.LEFT)

        opt_frame = ttk.LabelFrame(main, text="翻译设置", padding=8)
        opt_frame.pack(fill=tk.X, pady=(0, 8))

        row_chunk = ttk.Frame(opt_frame)
        row_chunk.pack(fill=tk.X, pady=2)
        ttk.Label(row_chunk, text="分块大小 (字):").pack(side=tk.LEFT)
        self.chunk_var = tk.IntVar(value=3000)
        ttk.Spinbox(row_chunk, from_=1000, to=8000, increment=500,
                     textvariable=self.chunk_var, width=8).pack(side=tk.LEFT, padx=8)

        row_target = ttk.Frame(opt_frame)
        row_target.pack(fill=tk.X, pady=2)
        ttk.Label(row_target, text="目标语言:").pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="中文")
        ttk.Combobox(row_target, textvariable=self.lang_var,
                     values=["中文", "English", "日本語", "한국어"],
                     state="readonly", width=10).pack(side=tk.LEFT, padx=8)

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill=tk.X, pady=(0, 8))

        self.start_btn = ttk.Button(btn_frame, text="开始翻译", command=self._start)
        self.start_btn.pack(side=tk.LEFT, padx=4)
        self.pause_btn = ttk.Button(btn_frame, text="暂停", command=self._pause, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=4)
        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self._stop, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=4)

        prog_frame = ttk.Frame(main)
        prog_frame.pack(fill=tk.X, pady=(0, 4))
        self.progress = ttk.Progressbar(prog_frame, mode="determinate")
        self.progress.pack(fill=tk.X, side=tk.LEFT, expand=True)
        self.progress_label = ttk.Label(prog_frame, text="就绪", width=20)
        self.progress_label.pack(side=tk.LEFT, padx=8)

        self.log = scrolledtext.ScrolledText(main, height=14, state=tk.DISABLED, wrap=tk.WORD)
        self.log.pack(fill=tk.BOTH, expand=True)

    def _on_api_change(self, _event=None):
        self._save_current_api()
        self._load_api_fields()

    def _load_api_fields(self):
        name = self.api_var.get()
        api = self.config["apis"].get(name, {})
        self.key_var.set(api.get("api_key", ""))
        self.url_var.set(api.get("base_url", DEFAULT_APIS.get(name, {}).get("base_url", "")))
        self.model_var.set(api.get("model", DEFAULT_APIS.get(name, {}).get("model", "")))

    def _save_current_api(self):
        name = self.api_var.get()
        self.config["apis"][name] = {
            "api_key": self.key_var.get(),
            "base_url": self.url_var.get(),
            "model": self.model_var.get()
        }
        self.config["last_used"] = name
        self._save_config()

    def _toggle_key(self):
        self.key_entry.config(show="" if self.show_key_var.get() else "*")

    def _on_mode_change(self):
        is_folder = self.mode_var.get() == "folder"
        self.file_entry.config(state=tk.DISABLED if is_folder else tk.NORMAL)
        self.file_btn.config(state=tk.DISABLED if is_folder else tk.NORMAL)
        self.dir_entry.config(state=tk.NORMAL if is_folder else tk.DISABLED)
        self.dir_btn.config(state=tk.NORMAL if is_folder else tk.DISABLED)

    def _browse_file(self):
        f = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
        if f:
            self.file_var.set(f)

    def _browse_dir(self):
        d = filedialog.askdirectory()
        if d:
            self.dir_var.set(d)

    def _log(self, msg: str):
        def _append():
            self.log.config(state=tk.NORMAL)
            self.log.insert(tk.END, msg + "\n")
            self.log.see(tk.END)
            self.log.config(state=tk.DISABLED)
        self.root.after(0, _append)

    def _set_progress(self, current: int, total: int, label: str = ""):
        def _update():
            self.progress["maximum"] = total
            self.progress["value"] = current
            if label:
                self.progress_label.config(text=label)
        self.root.after(0, _update)

    def _start(self):
        self._save_current_api()

        api_name = self.api_var.get()
        api_key = self.key_var.get().strip()
        base_url = self.url_var.get().strip()
        model = self.model_var.get().strip()

        if not api_key:
            messagebox.showerror("错误", "请填写 API Key")
            return
        if not base_url:
            messagebox.showerror("错误", "请填写 Base URL")
            return
        if not model:
            messagebox.showerror("错误", "请填写 Model")
            return

        mode = self.mode_var.get()
        if mode == "file":
            file_path = self.file_var.get().strip()
            if not file_path or not Path(file_path).is_file():
                messagebox.showerror("错误", "请选择有效的 MD 文件")
                return
            target = Path(file_path)
        else:
            input_dir = self.dir_var.get().strip()
            if not input_dir or not Path(input_dir).is_dir():
                messagebox.showerror("错误", "请选择有效的 MD 文件夹")
                return
            target = Path(input_dir)

        self.translator = Translator(APIConfig(
            name=api_name, base_url=base_url, model=model, api_key=api_key
        ))

        self.is_running = True
        self.is_paused = False
        self.should_stop = False
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)

        threading.Thread(target=self._run, args=(target, mode), daemon=True).start()

    def _pause(self):
        self.is_paused = not self.is_paused
        self.pause_btn.config(text="继续" if self.is_paused else "暂停")
        if self.is_paused:
            self._log("[暂停] 等待当前分块完成后暂停...")
        else:
            self._log("[继续] 恢复翻译...")

    def _stop(self):
        self.should_stop = True
        self._log("[停止] 等待当前分块完成后停止...")

    def _run(self, target: Path, mode: str):
        if mode == "file":
            md_files = [target]
            folder = target.parent
        else:
            folder = target
            md_files = sorted(folder.glob("*.md"))
            md_files = [f for f in md_files if not f.name.endswith(".translated.md")]

        if not md_files:
            self._log("未找到 .md 文件")
            self._finish()
            return

        self._log(f"共 {len(md_files)} 个 .md 文件待翻译")

        manifest_path = folder / ".translate_manifest.json"
        manifest_mgr = ManifestManager(manifest_path)

        pending = manifest_mgr.get_pending_files(md_files)
        already_done = len(md_files) - len(pending)
        if already_done > 0:
            self._log(f"跳过 {already_done} 个已翻译文件 (断点续传)")

        total = len(pending)
        success_count = 0
        fail_count = 0

        for idx, file_path in enumerate(pending):
            if self.should_stop:
                self._log("[停止] 翻译已停止")
                break

            while self.is_paused and not self.should_stop:
                import time
                time.sleep(0.5)

            if self.should_stop:
                break

            source_hash = self.translator._get_file_hash(file_path)
            output_path = file_path.with_name(
                file_path.stem + ".translated" + file_path.suffix
            )

            self._log(f"[{idx+1}/{total}] 翻译: {file_path.name}")
            self._set_progress(idx, total, f"{idx+1}/{total} {file_path.name}")

            def chunk_progress(cur, tot):
                label = f"[{idx+1}/{total}] {file_path.name} 分块 {cur}/{tot}"
                self._set_progress(cur, tot, label)

            result = self.translator.translate_file(
                file_path, output_path,
                manifest={"files": {}},
                max_chars_per_chunk=self.chunk_var.get(),
                progress_callback=chunk_progress
            )

            if result.success:
                manifest_mgr.mark_translated(file_path, source_hash)
                self._log(f"  OK -> {output_path.name}")
                success_count += 1
            else:
                self._log(f"  FAIL: {result.error}")
                fail_count += 1

        self._set_progress(total, total, "完成")
        self._log(f"翻译完成！成功: {success_count}, 失败: {fail_count}")
        self._finish()

    def _finish(self):
        self.is_running = False
        self.is_paused = False
        self.should_stop = False
        self.root.after(0, lambda: (
            self.start_btn.config(state=tk.NORMAL),
            self.pause_btn.config(state=tk.DISABLED, text="暂停"),
            self.stop_btn.config(state=tk.DISABLED)
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslateApp(root)
    root.mainloop()
