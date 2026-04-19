"""
Markdown 文件清洗工具
智能合并断行的段落，保留文档结构
"""

import re

def is_true_heading(line, next_line):
    """判断是否是真正的标题"""
    stripped = line.strip()
    if not stripped.startswith('#'):
        return False
    if next_line is not None and next_line.strip() == '':
        return True
    if 3 <= len(stripped.replace('#', '').strip()) <= 60 and \
       stripped.replace('#', '').strip().isupper():
        return True
    return False

def is_list_item(line):
    """判断是否是列表项"""
    stripped = line.strip()
    return bool(re.match(r'^[\s]*[-*+]\s', stripped) or re.match(r'^[\s]*\d+\.\s', stripped))

def is_special_line(line):
    """判断是否是需要单独保留的特殊行"""
    stripped = line.strip()
    if re.match(r'^[-*_]{3,}$', stripped):
        return True
    if stripped.startswith('>'):
        return True
    return False

def should_flush_paragraph(current_para, next_line):
    """判断是否应该flush当前段落"""
    if not current_para:
        return False
    
    current_text = ' '.join(current_para)
    next_stripped = next_line.strip() if next_line else ''
    
    # 如果当前段落已经有100+字符，考虑flush
    if len(current_text) >= 100:
        # 但如果下一行是句子的继续（以小写开头），继续累积
        if next_stripped and next_stripped[0].islower():
            return False
        return True
    
    return False

def process_markdown(content, remove_images=False):
    """
    清洗 Markdown 文件
    
    Args:
        content: 文件内容字符串
        remove_images: 是否删除图片引用，默认 False
    
    Returns:
        清洗后的内容
    """
    lines = content.split('\n')
    result = []
    current_paragraph = []
    
    n = len(lines)
    i = 0
    
    def flush_paragraph():
        nonlocal current_paragraph
        if current_paragraph:
            merged = ' '.join(current_paragraph)
            result.append(merged)
            current_paragraph = []
    
    while i < n:
        line = lines[i]
        next_line = lines[i + 1] if i + 1 < n else None
        stripped = line.strip()
        
        # 1. 跳过图片引用（可选）
        if remove_images and re.match(r'^!\[[^\]]*\]\([^)]*\.png\)$', stripped):
            i += 1
            continue
        
        # 2. 空行
        if not stripped:
            if should_flush_paragraph(current_paragraph, next_line):
                flush_paragraph()
            i += 1
            continue
        
        # 3. 真正的标题 - flush 段落，保留标题
        if is_true_heading(line, next_line):
            flush_paragraph()
            result.append(stripped)
            i += 1
            continue
        
        # 4. 特殊行（分隔线、引用）
        if is_special_line(line):
            flush_paragraph()
            result.append(stripped)
            i += 1
            continue
        
        # 5. 列表项 - flush 段落，保留列表项
        if is_list_item(line):
            flush_paragraph()
            result.append(stripped)
            i += 1
            continue
        
        # 6. 判断是否应该flush
        if should_flush_paragraph(current_paragraph, next_line):
            flush_paragraph()
        
        # 7. 累积内容
        current_paragraph.append(stripped)
        i += 1
    
    # 处理最后剩余的段落
    flush_paragraph()
    
    # 清理连续空行
    final = []
    prev_empty = False
    for line in result:
        current_empty = line.strip() == ''
        if current_empty:
            if not prev_empty:
                final.append('')
            prev_empty = True
        else:
            final.append(line)
            prev_empty = False
    
    return '\n'.join(final)


def main():
    """命令行用法示例"""
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python cleanup_markdown.py <输入文件> <输出文件> [--remove-images]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    remove_images = '--remove-images' in sys.argv
    
    print(f"读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"原始行数: {content.count(chr(10)) + 1}")
    
    image_count = len(re.findall(r'!\[[^\]]*\]\([^)]*\.png\)', content))
    print(f"图片数量: {image_count}")
    if remove_images:
        print("将删除图片引用")
    
    print("处理中...")
    cleaned = process_markdown(content, remove_images=remove_images)
    
    print(f"处理后行数: {cleaned.count(chr(10)) + 1}")
    
    print(f"保存文件: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    
    print("完成!")


if __name__ == '__main__':
    main()
