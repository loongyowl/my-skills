export function generateFrontmatter(metadata) {
  const { bookName, author, chapterName } = metadata;
  const date = new Date().toISOString().split('T')[0];

  const lines = [
    '---',
    `title: ${chapterName || '未命名章节'}`,
    `book: [[${bookName || '未知书籍'}]]`,
    `author: ${author || '未知作者'}`,
    `created: ${date}`,
    '---',
    '',
    ''
  ];

  return lines.join('\n');
}

export function combineOutput(frontmatter, content) {
  return frontmatter + content;
}

export function estimateWordCount(text) {
  if (!text) return 0;
  const chineseChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
  const englishWords = (text.match(/[a-zA-Z]+/g) || []).length;
  return chineseChars + Math.floor(englishWords / 2);
}

export function formatBookNameForObsidian(bookName) {
  if (!bookName) return '';
  if (bookName.startsWith('[[') && bookName.endsWith(']]')) {
    return bookName;
  }
  return `[[${bookName}]]`;
}

export function stripBookNameFormatting(bookName) {
  if (!bookName) return '';
  if (bookName.startsWith('[[') && bookName.endsWith(']]')) {
    return bookName.slice(2, -2);
  }
  return bookName;
}

export function downloadMarkdown(content, filename) {
  const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename.endsWith('.md') ? filename : `${filename}.md`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

export function copyToClipboard(text) {
  return navigator.clipboard.writeText(text);
}
