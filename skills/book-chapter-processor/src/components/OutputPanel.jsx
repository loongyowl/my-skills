import { useState, useEffect } from 'react';
import Editor from '@monaco-editor/react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export default function OutputPanel({ content, onChange, viewMode, onViewModeChange, disabled = false }) {
  const [localContent, setLocalContent] = useState(content);

  useEffect(() => {
    setLocalContent(content);
  }, [content]);

  const handleEditorChange = (value) => {
    setLocalContent(value || '');
    if (onChange) onChange(value || '');
  };

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center gap-1 mb-2">
        <button
          onClick={() => onViewModeChange('render')}
          className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
            viewMode === 'render'
              ? 'bg-indigo-100 text-indigo-700'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          渲染
        </button>
        <button
          onClick={() => onViewModeChange('source')}
          className={`px-3 py-1.5 text-xs font-medium rounded-lg transition-all ${
            viewMode === 'source'
              ? 'bg-indigo-100 text-indigo-700'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          源码
        </button>
      </div>

      <div className="flex-1 overflow-hidden rounded-xl border border-gray-100">
        {viewMode === 'render' ? (
          <div className="h-full overflow-auto bg-white p-4">
            {localContent ? (
              <div className="markdown-preview">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                  {localContent}
                </ReactMarkdown>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400 text-sm">
                处理后的内容将显示在这里
              </div>
            )}
          </div>
        ) : (
          <Editor
            height="100%"
            defaultLanguage="markdown"
            value={localContent}
            onChange={handleEditorChange}
            theme="vs"
            options={{
              minimap: { enabled: false },
              fontSize: 13,
              lineNumbers: 'off',
              folding: false,
              wordWrap: 'on',
              scrollBeyondLastLine: false,
              readOnly: disabled,
              automaticLayout: true,
              padding: { top: 12, bottom: 12 },
              scrollbar: {
                vertical: 'visible',
                horizontal: 'visible',
                verticalScrollbarSize: 8,
                horizontalScrollbarSize: 8
              }
            }}
          />
        )}
      </div>

      <div className="mt-2 text-xs text-gray-400 text-right">
        {localContent.length > 0 && `${localContent.length} 字符`}
      </div>
    </div>
  );
}
