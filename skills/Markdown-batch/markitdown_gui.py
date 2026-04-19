# -*- coding: utf-8 -*-
"""
MarkItDown 可视化转换工具
支持单文件 / 批量文件夹转换，支持 Word、PDF、PPT、Excel、HTML、CSV 等格式
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
from datetime import datetime

# ── 支持的格式 ──────────────────────────────────────────────
SUPPORTED_FORMATS = {
    "Word (.docx/.doc)":       [".docx", ".doc"],
    "PDF (.pdf)":              [".pdf"],
    "PowerPoint (.pptx/.ppt)": [".pptx", ".ppt"],
    "Excel (.xlsx/.xls)":      [".xlsx", ".xls"],
    "HTML 网页 (.html/.htm)":  [".html", ".htm"],
    "CSV 表格 (.csv)":         [".csv"],
    "JSON 数据 (.json)":       [".json"],
    "XML 文档 (.xml)":         [".xml"],
    "文本文件 (.txt)":          [".txt"],
    "全部支持格式":            [".docx", ".doc", ".pdf", ".pptx", ".ppt",
                                 ".xlsx", ".xls", ".html", ".htm",
                                 ".csv", ".json", ".xml", ".txt"],
}


# ── 主 GUI 类 ────────────────────────────────────────────────
class MarkItDownApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MarkItDown 文档转 Markdown 工具")
        self.geometry("750x620")
        self.resizable(True, True)
        self.configure(bg="#f5f5f5")

        # 主题色
        self.accent = "#0078D4"   # 微软蓝

        self._build_ui()
        self._apply_styles()

    # ── 构建 UI ──────────────────────────────────────────────
    def _build_ui(self):
        # 标题栏
        header = tk.Frame(self, bg=self.accent, height=56)
        header.pack(fill="x")
        tk.Label(
            header, text="📄  MarkItDown  文档 → Markdown 转换工具",
            bg=self.accent, fg="white",
            font=("微软雅黑", 14, "bold")
        ).pack(side="left", padx=20, pady=12)

        # 主体内容
        body = tk.Frame(self, bg="#f5f5f5")
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # ── 模式选择 ──────────────────────────────────────────
        mode_frame = self._section(body, "📁  转换模式")
        self.mode_var = tk.StringVar(value="single")
        rb1 = ttk.Radiobutton(mode_frame, text="单个文件转换",
                               variable=self.mode_var, value="single",
                               command=self._on_mode_change)
        rb2 = ttk.Radiobutton(mode_frame, text="批量文件夹转换",
                               variable=self.mode_var, value="batch",
                               command=self._on_mode_change)
        rb1.pack(side="left", padx=(0, 20))
        rb2.pack(side="left")

        # ── 格式选择 ──────────────────────────────────────────
        fmt_frame = self._section(body, "🗂  文件格式")
        self.fmt_var = tk.StringVar(value="Word (.docx/.doc)")
        fmt_combo = ttk.Combobox(
            fmt_frame, textvariable=self.fmt_var,
            values=list(SUPPORTED_FORMATS.keys()),
            state="readonly", width=36, font=("微软雅黑", 10)
        )
        fmt_combo.pack(side="left")

        # ── 输入路径 ──────────────────────────────────────────
        in_frame = self._section(body, "📂  输入路径")
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(in_frame, textvariable=self.input_var,
                                     font=("微软雅黑", 10), width=52)
        self.input_entry.pack(side="left", padx=(0, 8))
        self.btn_browse_in = ttk.Button(in_frame, text="浏览…",
                                         command=self._browse_input, width=8)
        self.btn_browse_in.pack(side="left")

        # ── 输出目录 ──────────────────────────────────────────
        out_frame = self._section(body, "💾  输出目录")
        self.output_var = tk.StringVar()
        ttk.Entry(out_frame, textvariable=self.output_var,
                  font=("微软雅黑", 10), width=52).pack(side="left", padx=(0, 8))
        ttk.Button(out_frame, text="浏览…",
                   command=self._browse_output, width=8).pack(side="left")
        tk.Label(out_frame, text="（留空则与原文件同目录）",
                 bg="#f5f5f5", fg="#888", font=("微软雅黑", 9)).pack(side="left", padx=8)

        # ── 选项 ──────────────────────────────────────────────
        opt_frame = self._section(body, "⚙️  选项")
        self.recursive_var = tk.BooleanVar(value=True)
        self.recursive_cb = ttk.Checkbutton(
            opt_frame, text="子目录递归（批量模式有效）",
            variable=self.recursive_var)
        self.recursive_cb.pack(side="left", padx=(0, 20))

        self.overwrite_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_frame, text="覆盖已存在的 .md 文件",
                        variable=self.overwrite_var).pack(side="left")

        # ── 转换按钮 ──────────────────────────────────────────
        btn_row = tk.Frame(body, bg="#f5f5f5")
        btn_row.pack(fill="x", pady=(8, 4))
        self.btn_convert = tk.Button(
            btn_row, text="▶  开始转换", bg=self.accent, fg="white",
            font=("微软雅黑", 11, "bold"), relief="flat",
            padx=24, pady=8, cursor="hand2",
            command=self._start_convert
        )
        self.btn_convert.pack(side="left")
        self.btn_clear = tk.Button(
            btn_row, text="🗑  清空日志", bg="#e0e0e0", fg="#333",
            font=("微软雅黑", 10), relief="flat",
            padx=16, pady=8, cursor="hand2",
            command=self._clear_log
        )
        self.btn_clear.pack(side="left", padx=(12, 0))

        # 进度条
        self.progress = ttk.Progressbar(body, mode="determinate")
        self.progress.pack(fill="x", pady=(4, 0))

        # ── 日志区 ──────────────────────────────────────────
        log_label = tk.Label(body, text="📋  转换日志",
                              bg="#f5f5f5", fg="#333",
                              font=("微软雅黑", 10, "bold"))
        log_label.pack(anchor="w", pady=(10, 2))
        self.log = scrolledtext.ScrolledText(
            body, height=10, font=("Consolas", 9),
            bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white", relief="flat"
        )
        self.log.pack(fill="both", expand=True)
        self.log.tag_config("ok",    foreground="#4ec9b0")
        self.log.tag_config("err",   foreground="#f48771")
        self.log.tag_config("info",  foreground="#9cdcfe")
        self.log.tag_config("warn",  foreground="#dcdcaa")

    def _section(self, parent, label_text):
        """创建带标签的区块，返回内容 Frame"""
        wrap = tk.Frame(parent, bg="#f5f5f5")
        wrap.pack(fill="x", pady=(0, 8))
        tk.Label(wrap, text=label_text, bg="#f5f5f5", fg="#333",
                 font=("微软雅黑", 10, "bold"), width=20, anchor="w"
                 ).pack(side="left")
        content = tk.Frame(wrap, bg="#f5f5f5")
        content.pack(side="left", fill="x", expand=True)
        return content

    def _apply_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox", padding=4)
        style.configure("TEntry", padding=4)
        style.configure("TRadiobutton", background="#f5f5f5",
                        font=("微软雅黑", 10))
        style.configure("TCheckbutton", background="#f5f5f5",
                        font=("微软雅黑", 10))
        style.configure("Horizontal.TProgressbar",
                        troughcolor="#e0e0e0", background=self.accent)

    # ── 事件处理 ──────────────────────────────────────────────
    def _on_mode_change(self):
        pass  # 模式切换时浏览按钮自适应

    def _browse_input(self):
        if self.mode_var.get() == "single":
            exts = SUPPORTED_FORMATS.get(self.fmt_var.get(), [])
            ft = [("支持的文档", " ".join(f"*{e}" for e in exts)),
                  ("所有文件", "*.*")]
            path = filedialog.askopenfilename(
                title="选择文件", filetypes=ft)
        else:
            path = filedialog.askdirectory(title="选择要转换的文件夹")
        if path:
            self.input_var.set(path)

    def _browse_output(self):
        path = filedialog.askdirectory(title="选择输出目录")
        if path:
            self.output_var.set(path)

    def _log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert("end", f"[{ts}] {msg}\n", tag)
        self.log.see("end")

    def _clear_log(self):
        self.log.delete("1.0", "end")

    # ── 转换逻辑 ──────────────────────────────────────────────
    def _start_convert(self):
        inp = self.input_var.get().strip()
        if not inp:
            messagebox.showwarning("提示", "请先选择输入文件或文件夹！")
            return

        self.btn_convert.config(state="disabled", text="转换中…")
        self.progress["value"] = 0
        threading.Thread(target=self._do_convert, daemon=True).start()

    def _do_convert(self):
        try:
            from markitdown import MarkItDown
        except ImportError:
            self._log("❌ 未找到 markitdown，请先运行 pip install markitdown", "err")
            self.btn_convert.config(state="normal", text="▶  开始转换")
            return

        md = MarkItDown()
        inp = self.input_var.get().strip()
        out_base = self.output_var.get().strip()
        exts = SUPPORTED_FORMATS.get(self.fmt_var.get(), [])

        # 收集文件列表
        if self.mode_var.get() == "single":
            files = [Path(inp)]
        else:
            src = Path(inp)
            pattern = "**/*" if self.recursive_var.get() else "*"
            files = [f for f in src.glob(pattern)
                     if f.is_file() and f.suffix.lower() in exts]

        if not files:
            self._log("⚠️ 未找到符合条件的文件，请检查路径和格式设置。", "warn")
            self.btn_convert.config(state="normal", text="▶  开始转换")
            return

        total = len(files)
        self._log(f"🔍 共找到 {total} 个文件，开始转换…", "info")

        ok_count = 0
        err_count = 0

        for i, src_file in enumerate(files, 1):
            # 确定输出路径
            if out_base:
                if self.mode_var.get() == "batch":
                    try:
                        rel = src_file.relative_to(Path(inp))
                    except ValueError:
                        rel = Path(src_file.name)
                    out_file = Path(out_base) / rel.with_suffix(".md")
                else:
                    out_file = Path(out_base) / (src_file.stem + ".md")
            else:
                out_file = src_file.with_suffix(".md")

            # 跳过已存在
            if out_file.exists() and not self.overwrite_var.get():
                self._log(f"⏭ 跳过（已存在）: {src_file.name}", "warn")
                self.progress["value"] = int(i / total * 100)
                continue

            # 创建输出目录
            out_file.parent.mkdir(parents=True, exist_ok=True)

            try:
                result = md.convert(str(src_file))
                out_file.write_text(result.text_content, encoding="utf-8")
                self._log(f"✅ [{i}/{total}] {src_file.name} → {out_file.name}", "ok")
                ok_count += 1
            except Exception as e:
                err_str = str(e)
                # 给常见错误提供更友好的提示
                if "BadZipFile" in err_str or "not a zip file" in err_str.lower():
                    reason = "文件格式异常（可能是旧版.doc改名、文件损坏或加密）"
                elif "PasswordProtected" in err_str or "password" in err_str.lower():
                    reason = "文件有密码保护，无法读取"
                elif "Permission" in err_str:
                    reason = "文件被占用或无读取权限"
                else:
                    reason = err_str[:120]   # 截断超长错误信息
                self._log(f"⚠️ [{i}/{total}] 跳过 {src_file.name}  原因: {reason}", "err")
                err_count += 1

            self.progress["value"] = int(i / total * 100)

        summary_tag = "ok" if err_count == 0 else "warn"
        self._log(
            f"\n{'🎉' if err_count == 0 else '⚠️'} 完成！"
            f"成功 {ok_count} 个 / 跳过失败 {err_count} 个 / 共 {total} 个",
            summary_tag
        )
        if err_count > 0:
            self._log(
                "💡 提示：失败文件可能是旧版二进制 .doc 格式改名为 .docx，"
                "请用 Word 另存为标准 .docx 后重试。", "warn"
            )
        self.btn_convert.config(state="normal", text="▶  开始转换")


# ── 入口 ────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        app = MarkItDownApp()
        app.mainloop()
    except KeyboardInterrupt:
        pass  # 防止命令行误触 Ctrl+C 导致崩溃
