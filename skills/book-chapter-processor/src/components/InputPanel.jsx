import { useRef, useEffect } from 'react';

export default function InputPanel({ value, onChange, placeholder = '粘贴原始文本...', disabled = false }) {
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [value]);

  return (
    <div className="h-full flex flex-col">
      <textarea
        ref={textareaRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        disabled={disabled}
        className="flex-1 w-full p-4 text-sm text-gray-800 bg-gray-50 border border-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none disabled:opacity-60 disabled:cursor-not-allowed"
        style={{ minHeight: '200px' }}
      />
      <div className="mt-2 text-xs text-gray-400 text-right">
        {value.length > 0 && `${value.length} 字符`}
      </div>
    </div>
  );
}
