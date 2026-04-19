# -*- coding: utf-8 -*-
"""
批量 .doc → .docx 转换工具
原理：调用本机 Microsoft Word，逐个打开 .doc 并另存为 .docx
依赖：pywin32（pip install pywin32）、本机已安装 Microsoft Word
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import threading
import os
import sys
from pathlib import Path
from datetime import datetime


class DocConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("批量 .doc → .docx 转换工具")
        self.geometry("680x520")
        self.resizable(True, True)
        self.configure(bg="#f5f5f5")
        self.accent = "#107C10"   # 绿色（Word 品牌色）
        self._build_ui()
        self._apply_styles()

    # ── UI 构建 ───────────────────────────────────────────────
    def _build_ui(self):
        # 标题栏
        hdr = tk.Frame(self, bg=self.accent, height=52)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📝  批量 .doc → .docx 转换工具",
                 bg=self.accent, fg="white",
                 font=("微软雅黑", 13, "bold")).pack(side="left", padx=20, pady=12)

        body = tk.Frame(self, bg="#f5f5f5")
        body.pack(fill="both", expand=True, padx=20, pady=16)

        # ── 输入目录 ──────────────────────────────────────────
        in_row = self._section(body, "📂  输入文件夹")
        self.input_var = tk.StringVar()
        ttk.Entry(in_row, textvariable=self.input_var,
                  font=("微软雅黑", 10), width=50).pack(side="left", padx=(0, 8))
        ttk.Button(in_row, text="浏览…",
                   command=self._browse_input, width=8).pack(side="left")

        # ── 输出目录 ──────────────────────────────────────────
        out_row = self._section(body, "💾  输出文件夹")
        self.output_var = tk.StringVar()
        ttk.Entry(out_row, textvariable=self.output_var,
                  font=("微软雅黑", 10), width=50).pack(side="left", padx=(0, 8))
        ttk.Button(out_row, text="浏览…",
                   command=self._browse_output, width=8).pack(side="left")
        tk.Label(out_row, text="（留空则与原文件同目录）",
                 bg="#f5f5f5", fg="#888",
                 font=("微软雅黑", 9)).pack(side="left", padx=6)

        # ── 选项 ──────────────────────────────────────────────
        opt_row = self._section(body, "⚙️  选项")
        self.recursive_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_row, text="递归子目录",
                        variable=self.recursive_var).pack(side="left", padx=(0, 20))
        self.overwrite_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_row, text="覆盖已存在的 .docx",
                        variable=self.overwrite_var).pack(side="left", padx=(0, 20))
        self.delete_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(opt_row, text="转换成功后删除原 .doc",
                        variable=self.delete_var).pack(side="left")

        # ── 按钮区 ────────────────────────────────────────────
        btn_row = tk.Frame(body, bg="#f5f5f5")
        btn_row.pack(fill="x", pady=(10, 4))
        self.btn_start = tk.Button(
            btn_row, text="▶  开始转换",
            bg=self.accent, fg="white",
            font=("微软雅黑", 11, "bold"), relief="flat",
            padx=24, pady=8, cursor="hand2",
            command=self._start)
        self.btn_start.pack(side="left")
        tk.Button(
            btn_row, text="🗑  清空日志",
            bg="#e0e0e0", fg="#333",
            font=("微软雅黑", 10), relief="flat",
            padx=16, pady=8, cursor="hand2",
            command=lambda: self.log.delete("1.0", "end")
        ).pack(side="left", padx=(12, 0))

        # 进度条
        self.progress = ttk.Progressbar(body, mode="determinate")
        self.progress.pack(fill="x", pady=(4, 0))

        # ── 日志 ──────────────────────────────────────────────
        tk.Label(body, text="📋  转换日志",
                 bg="#f5f5f5", fg="#333",
                 font=("微软雅黑", 10, "bold")).pack(anchor="w", pady=(10, 2))
        self.log = scrolledtext.ScrolledText(
            body, height=10, font=("Consolas", 9),
            bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white", relief="flat")
        self.log.pack(fill="both", expand=True)
        self.log.tag_config("ok",   foreground="#4ec9b0")
        self.log.tag_config("err",  foreground="#f48771")
        self.log.tag_config("info", foreground="#9cdcfe")
        self.log.tag_config("warn", foreground="#dcdcaa")

    def _section(self, parent, label):
        row = tk.Frame(parent, bg="#f5f5f5")
        row.pack(fill="x", pady=(0, 8))
        tk.Label(row, text=label, bg="#f5f5f5", fg="#333",
                 font=("微软雅黑", 10, "bold"), width=18,
                 anchor="w").pack(side="left")
        content = tk.Frame(row, bg="#f5f5f5")
        content.pack(side="left", fill="x", expand=True)
        return content

    def _apply_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("TCheckbutton", background="#f5f5f5", font=("微软雅黑", 10))
        s.configure("Horizontal.TProgressbar",
                    troughcolor="#e0e0e0", background=self.accent)

    # ── 事件 ─────────────────────────────────────────────────
    def _browse_input(self):
        p = filedialog.askdirectory(title="选择包含 .doc 文件的文件夹")
        if p:
            self.input_var.set(p)

    def _browse_output(self):
        p = filedialog.askdirectory(title="选择输出文件夹")
        if p:
            self.output_var.set(p)

    def _log(self, msg, tag="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.insert("end", f"[{ts}] {msg}\n", tag)
        self.log.see("end")

    def _start(self):
        inp = self.input_var.get().strip()
        if not inp:
            messagebox.showwarning("提示", "请先选择输入文件夹！")
            return
        if not Path(inp).is_dir():
            messagebox.showwarning("提示", "输入路径不是有效文件夹！")
            return
        self.btn_start.config(state="disabled", text="转换中…")
        self.progress["value"] = 0
        threading.Thread(target=self._do_convert, daemon=True).start()

    # ── 转换逻辑 ──────────────────────────────────────────────
    def _do_convert(self):
        try:
            import win32com.client
            import pywintypes
        except ImportError:
            self._log("❌ 未找到 pywin32，请运行：pip install pywin32", "err")
            self.btn_start.config(state="normal", text="▶  开始转换")
            return

        inp = Path(self.input_var.get().strip())
        out_base = self.output_var.get().strip()
        pattern = "**/*.doc" if self.recursive_var.get() else "*.doc"

        # 收集所有 .doc 文件（排除已经是 .docx 的）
        files = [f for f in inp.glob(pattern)
                 if f.is_file() and f.suffix.lower() == ".doc"]

        if not files:
            self._log("⚠️ 未找到任何 .doc 文件，请检查路径和选项。", "warn")
            self.btn_start.config(state="normal", text="▶  开始转换")
            return

        total = len(files)
        self._log(f"🔍 共找到 {total} 个 .doc 文件，正在启动 Word…", "info")

        # 启动 Word（不显示界面，后台静默运行）
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            word.DisplayAlerts = False
        except Exception as e:
            self._log(f"❌ 无法启动 Microsoft Word：{e}", "err")
            self._log("💡 请确认本机已安装 Microsoft Word（非 WPS）。", "warn")
            self.btn_start.config(state="normal", text="▶  开始转换")
            return

        ok_count = 0
        err_count = 0
        skip_count = 0

        try:
            for i, doc_path in enumerate(files, 1):
                # 确定输出路径
                if out_base:
                    if self.recursive_var.get():
                        try:
                            rel = doc_path.relative_to(inp)
                        except ValueError:
                            rel = Path(doc_path.name)
                        out_file = Path(out_base) / rel.with_suffix(".docx")
                    else:
                        out_file = Path(out_base) / (doc_path.stem + ".docx")
                else:
                    out_file = doc_path.with_suffix(".docx")

                # 跳过已存在
                if out_file.exists() and not self.overwrite_var.get():
                    self._log(f"⏭ [{i}/{total}] 跳过（.docx 已存在）: {doc_path.name}", "warn")
                    skip_count += 1
                    self.progress["value"] = int(i / total * 100)
                    continue

                # 创建输出目录
                out_file.parent.mkdir(parents=True, exist_ok=True)

                try:
                    # 用绝对路径打开（Word 需要绝对路径）
                    doc = word.Documents.Open(
                        str(doc_path.resolve()),
                        ReadOnly=True,
                        AddToRecentFiles=False
                    )
                    # 16 = wdFormatXMLDocument (.docx)
                    doc.SaveAs2(
                        str(out_file.resolve()),
                        FileFormat=16
                    )
                    doc.Close(SaveChanges=False)

                    self._log(
                        f"✅ [{i}/{total}] {doc_path.name} → {out_file.name}", "ok")
                    ok_count += 1

                    # 可选：删除原文件
                    if self.delete_var.get():
                        try:
                            doc_path.unlink()
                            self._log(f"   🗑 已删除原文件: {doc_path.name}", "warn")
                        except Exception as del_e:
                            self._log(f"   ⚠️ 删除原文件失败: {del_e}", "err")

                except Exception as e:
                    err_msg = str(e)
                    if "password" in err_msg.lower() or "Password" in err_msg:
                        reason = "文件有密码保护"
                    elif "permission" in err_msg.lower():
                        reason = "文件被占用或无权限"
                    else:
                        reason = err_msg[:100]
                    self._log(
                        f"⚠️ [{i}/{total}] 跳过 {doc_path.name}  原因: {reason}", "err")
                    err_count += 1
                    # 确保文档已关闭
                    try:
                        word.Documents.Close()
                    except Exception:
                        pass

                self.progress["value"] = int(i / total * 100)

        finally:
            # 无论是否出错，都关闭 Word 进程
            try:
                word.Quit()
            except Exception:
                pass

        tag = "ok" if err_count == 0 else "warn"
        self._log(
            f"\n{'🎉' if err_count == 0 else '⚠️'} 完成！"
            f"成功 {ok_count} 个 / 失败 {err_count} 个 / 跳过 {skip_count} 个 / 共 {total} 个",
            tag
        )
        self.btn_start.config(state="normal", text="▶  开始转换")


# ── 入口 ─────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        app = DocConverterApp()
        app.mainloop()
    except KeyboardInterrupt:
        pass
