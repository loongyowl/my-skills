"""批量转换目录下所有 PDF 为 Markdown
路径基于本脚本所在位置（skills/pdf-to-markdown/scripts/）动态解析，
无需修改任何硬编码路径。
"""
import subprocess, sys, os, glob, time

try:
    import pymupdf
except ImportError:
    pymupdf = None

# --- 路径定位 ---
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR   = os.path.dirname(SCRIPTS_DIR)
DEPS_DIR    = os.path.join(SKILL_DIR, 'dependencies')

_jdk_bundled = os.path.join(DEPS_DIR, 'jdk')
_cli_bundled = os.path.join(DEPS_DIR, 'opendataloader-pdf.exe')

JAVA_HOME = _jdk_bundled if os.path.isdir(_jdk_bundled) else \
    r'C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64'

CLI = _cli_bundled if os.path.isfile(_cli_bundled) else \
    r'C:\Users\JoeHuang\AppData\Roaming\Python\Python314\Scripts\opendataloader-pdf.exe'

sys.stdout.reconfigure(encoding='utf-8')


def get_env():
    env = os.environ.copy()
    env['JAVA_HOME'] = JAVA_HOME
    env['PATH'] = os.path.join(JAVA_HOME, 'bin') + os.pathsep + env['PATH']
    return env


def is_native_text(pdf_path):
    """检测是否为原生文本 PDF（需要 pymupdf）"""
    if pymupdf is None:
        return True  # 无法检测时默认当原生处理
    try:
        doc = pymupdf.open(pdf_path)
        texts = [len(doc[i].get_text().strip()) for i in range(min(3, len(doc)))]
        doc.close()
        return sum(texts) / len(texts) > 50 if texts else False
    except Exception:
        return False


def convert_pdf(pdf_path, output_dir):
    """用 OpenDataLoader 转换原生文本 PDF"""
    r = subprocess.run(
        [CLI, pdf_path, '-f', 'markdown', '-o', output_dir],
        capture_output=True, text=True, encoding='utf-8',
        env=get_env(), timeout=300
    )
    return r.returncode == 0


def batch_convert(pdf_dir, output_dir=None):
    if not os.path.exists(pdf_dir):
        print(f"目录不存在: {pdf_dir}")
        return

    if output_dir is None:
        output_dir = pdf_dir

    os.makedirs(output_dir, exist_ok=True)

    pdfs = glob.glob(os.path.join(pdf_dir, '*.pdf'))
    pdfs = [p for p in pdfs if not os.path.basename(p).startswith('~$')]

    if not pdfs:
        print("未找到 PDF 文件")
        return

    print(f"找到 {len(pdfs)} 个 PDF 文件")
    print(f"输出目录: {output_dir}")
    print("-" * 50)

    success, fail = 0, []

    for pdf in pdfs:
        name = os.path.basename(pdf)
        is_native = is_native_text(pdf)
        type_label = "原生" if is_native else "扫描"

        if not is_native:
            print(f"[跳过 扫描版] {name}")
            continue

        print(f"[{type_label}] {name} ...", end=' ', flush=True)
        start = time.time()
        ok = convert_pdf(pdf, output_dir)
        elapsed = time.time() - start

        if ok:
            md_name = name.replace('.pdf', '.md')
            md_path = os.path.join(output_dir, md_name)
            size = os.path.getsize(md_path) // 1024 if os.path.exists(md_path) else 0
            print(f"OK ({size} KB, {elapsed:.1f}s)")
            success += 1
        else:
            print("失败")
            fail.append(name)

    print("-" * 50)
    print(f"完成: {success} 成功, {len(fail)} 失败")
    if fail:
        print("失败文件:", ', '.join(fail))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python batch_convert.py <PDF目录> [输出目录]")
        sys.exit(1)

    pdf_dir = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    batch_convert(pdf_dir, out_dir)
