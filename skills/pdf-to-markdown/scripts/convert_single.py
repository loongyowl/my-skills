"""将单个 PDF 转换为 Markdown
路径基于本脚本所在位置（skills/pdf-to-markdown/scripts/）动态解析，
无需修改任何硬编码路径。
"""
import subprocess, sys, os

# --- 路径定位 ---
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR   = os.path.dirname(SCRIPTS_DIR)
DEPS_DIR    = os.path.join(SKILL_DIR, 'dependencies')

# 优先用技能包内的 dependencies，回退到用户级安装
_jdk_bundled = os.path.join(DEPS_DIR, 'jdk')
_cli_bundled = os.path.join(DEPS_DIR, 'opendataloader-pdf.exe')

JAVA_HOME = _jdk_bundled if os.path.isdir(_jdk_bundled) else \
    r'C:\Users\JoeHuang\WorkBuddy\Claw\openlogic-openjdk-21.0.5+11-windows-x64'

CLI = _cli_bundled if os.path.isfile(_cli_bundled) else \
    r'C:\Users\JoeHuang\AppData\Roaming\Python\Python314\Scripts\opendataloader-pdf.exe'


def get_java_env():
    env = os.environ.copy()
    env['JAVA_HOME'] = JAVA_HOME
    env['PATH'] = os.path.join(JAVA_HOME, 'bin') + os.pathsep + env['PATH']
    return env


def convert(pdf_path, output_dir=None, fmt='markdown'):
    sys.stdout.reconfigure(encoding='utf-8')

    if not os.path.exists(pdf_path):
        print(f"文件不存在: {pdf_path}")
        return False

    if output_dir is None:
        output_dir = os.path.dirname(pdf_path)

    os.makedirs(output_dir, exist_ok=True)

    print(f"开始转换: {os.path.basename(pdf_path)}")
    r = subprocess.run(
        [CLI, pdf_path, '-f', fmt, '-o', output_dir],
        capture_output=True, text=True, encoding='utf-8',
        env=get_java_env(), timeout=300
    )

    if r.returncode != 0:
        print(f"转换失败: {r.stderr}")
        return False

    md_name = os.path.basename(pdf_path).replace('.pdf', '.md')
    md_path = os.path.join(output_dir, md_name)
    size = os.path.getsize(md_path) // 1024 if os.path.exists(md_path) else 0
    print(f"完成: {md_name} ({size} KB)")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python convert_single.py <pdf文件> [输出目录] [格式]")
        print("  格式: markdown (默认) | json")
        sys.exit(1)

    pdf = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    fmt = sys.argv[3] if len(sys.argv) > 3 else 'markdown'
    convert(pdf, out, fmt)
