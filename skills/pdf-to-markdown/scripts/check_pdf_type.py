"""检测 PDF 类型：原生文本 vs 扫描版"""
import pymupdf, sys, os

sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv) < 2:
    print("用法: python check_pdf_type.py <pdf文件路径>")
    sys.exit(1)

pdf = sys.argv[1]
if not os.path.exists(pdf):
    print(f"文件不存在: {pdf}")
    sys.exit(1)

doc = pymupdf.open(pdf)
pages = len(doc)
texts = [len(doc[i].get_text().strip()) for i in range(min(3, pages))]
avg = sum(texts) / len(texts) if texts else 0
doc.close()

if avg > 50:
    type_ = "原生文本 PDF"
elif avg < 30:
    type_ = "扫描版 PDF（需要 OCR）"
else:
    type_ = "混合型 PDF"

print(f"{type_} | {pages}页 | 均字量:{avg:.0f} | {os.path.basename(pdf)}")
