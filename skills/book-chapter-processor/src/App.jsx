import { useState, useCallback } from 'react';
import { Settings, FileText, Copy, Download, Loader2, CheckCircle, AlertCircle, Trash2 } from 'lucide-react';
import SettingsModal from './components/SettingsModal';
import TemplateModal from './components/TemplateModal';
import InputPanel from './components/InputPanel';
import OutputPanel from './components/OutputPanel';
import { useLocalStorage } from './hooks/useLocalStorage';
import { processWithLLM } from './hooks/useLlm';
import { TEMPLATES } from './constants/prompts';
import { generateFrontmatter, combineOutput, downloadMarkdown, copyToClipboard, estimateWordCount } from './utils/markdown';

export default function App() {
  const [config, setConfig] = useLocalStorage('book-processor-config', {
    provider: 'deepseek',
    apiKey: '',
    baseUrl: 'https://api.deepseek.com/v1',
    model: 'deepseek-chat'
  });

  const [metadata, setMetadata] = useLocalStorage('book-processor-metadata', {
    bookName: '',
    author: '',
    chapterName: ''
  });

  const [templateId, setTemplateId] = useLocalStorage('book-processor-template', 'deep-note');
  const [customPrompt, setCustomPrompt] = useLocalStorage('book-processor-custom-prompt', '');

  const [input, setInput] = useLocalStorage('book-processor-input', '');
  const [output, setOutput] = useState('');
  const [viewMode, setViewMode] = useState('render');

  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);
  const [copySuccess, setCopySuccess] = useState(false);

  const [settingsOpen, setSettingsOpen] = useState(false);
  const [templateOpen, setTemplateOpen] = useState(false);

  const selectedTemplate = TEMPLATES.find(t => t.id === templateId) || TEMPLATES[0];

  const handleProcess = useCallback(async () => {
    if (!input.trim()) {
      setError('请输入原始文本');
      return;
    }
    if (!config.apiKey) {
      setError('请先配置 API Key');
      setSettingsOpen(true);
      return;
    }

    setIsProcessing(true);
    setError(null);
    setProgress({ status: 'starting', message: '准备处理...' });

    try {
      const systemPrompt = customPrompt || selectedTemplate.prompt;

      const result = await processWithLLM({
        config,
        systemPrompt,
        userContent: input,
        metadata,
        onProgress: setProgress
      });

      const frontmatter = generateFrontmatter(metadata);
      const fullOutput = combineOutput(frontmatter, result);

      setOutput(fullOutput);
      setProgress(null);
    } catch (err) {
      setError(err.message);
      setProgress(null);
    } finally {
      setIsProcessing(false);
    }
  }, [input, config, metadata, customPrompt, selectedTemplate]);

  const handleCopy = useCallback(async () => {
    if (!output) return;
    try {
      await copyToClipboard(output);
      setCopySuccess(true);
      setTimeout(() => setCopySuccess(false), 2000);
    } catch (err) {
      setError('复制失败');
    }
  }, [output]);

  const handleDownload = useCallback(() => {
    if (!output) return;
    const filename = metadata.chapterName || 'output';
    downloadMarkdown(output, filename);
  }, [output, metadata.chapterName]);

  const inputWordCount = estimateWordCount(input);
  const outputWordCount = estimateWordCount(output);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-white border-b border-gray-100 px-6 py-3">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold text-gray-900">高保真书籍章节加工器</h1>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSettingsOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all"
            >
              <Settings size={14} />
              API设置
            </button>
            <button
              onClick={() => setTemplateOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-all"
            >
              <FileText size={14} />
              模板: {selectedTemplate.name}
            </button>
          </div>
        </div>
      </header>

      <div className="flex-1 flex flex-col px-6 py-4 gap-4">
        <div className="bg-white rounded-xl border border-gray-100 p-4">
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">书名</label>
              <input
                type="text"
                value={metadata.bookName}
                onChange={(e) => setMetadata({ ...metadata, bookName: e.target.value })}
                placeholder="输入书名"
                className="w-full px-3 py-2 text-sm bg-gray-50 border border-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">作者</label>
              <input
                type="text"
                value={metadata.author}
                onChange={(e) => setMetadata({ ...metadata, author: e.target.value })}
                placeholder="输入作者"
                className="w-full px-3 py-2 text-sm bg-gray-50 border border-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-gray-500 mb-1">章节名</label>
              <input
                type="text"
                value={metadata.chapterName}
                onChange={(e) => setMetadata({ ...metadata, chapterName: e.target.value })}
                placeholder="输入章节名"
                className="w-full px-3 py-2 text-sm bg-gray-50 border border-gray-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
            </div>
          </div>
        </div>

        <div className="flex-1 grid grid-cols-2 gap-4 min-h-0">
          <div className="bg-white rounded-xl border border-gray-100 p-4 flex flex-col">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-medium text-gray-500">原始文本</span>
              {inputWordCount > 0 && (
                <span className="text-xs text-gray-400">{inputWordCount} 字</span>
              )}
            </div>
            <div className="flex-1 min-h-0">
              <InputPanel
                value={input}
                onChange={setInput}
                disabled={isProcessing}
              />
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-100 p-4 flex flex-col">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium text-gray-500">输出结果</span>
                {outputWordCount > 0 && (
                  <span className="text-xs text-gray-400">{outputWordCount} 字</span>
                )}
              </div>
              {output && (
                <button
                  onClick={() => { setOutput(''); setError(null); }}
                  disabled={isProcessing}
                  className="flex items-center gap-1 px-2 py-1 text-xs font-medium text-red-500 bg-red-50 rounded-lg hover:bg-red-100 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                >
                  <Trash2 size={12} />
                  清空
                </button>
              )}
            </div>
            <div className="flex-1 min-h-0">
              <OutputPanel
                content={output}
                onChange={setOutput}
                viewMode={viewMode}
                onViewModeChange={setViewMode}
                disabled={isProcessing}
              />
            </div>
          </div>
        </div>

        {error && (
          <div className="flex items-center gap-2 px-4 py-3 bg-red-50 border border-red-100 rounded-xl text-sm text-red-700">
            <AlertCircle size={16} />
            {error}
          </div>
        )}

        {progress && (
          <div className="flex items-center gap-2 px-4 py-3 bg-indigo-50 border border-indigo-100 rounded-xl text-sm text-indigo-700">
            <Loader2 size={16} className="animate-spin" />
            {progress.message}
          </div>
        )}
      </div>

      <footer className="bg-white border-t border-gray-100 px-6 py-3">
        <div className="flex items-center justify-between">
          <button
            onClick={handleProcess}
            disabled={isProcessing || !input.trim()}
            className="flex items-center gap-2 px-6 py-2.5 text-sm font-medium text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {isProcessing ? (
              <>
                <Loader2 size={14} className="animate-spin" />
                处理中...
              </>
            ) : (
              '开始加工'
            )}
          </button>
          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              disabled={!output}
              className="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {copySuccess ? <CheckCircle size={14} className="text-green-600" /> : <Copy size={14} />}
              {copySuccess ? '已复制' : '复制'}
            </button>
            <button
              onClick={handleDownload}
              disabled={!output}
              className="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              <Download size={14} />
              下载
            </button>
          </div>
        </div>
      </footer>

      <SettingsModal
        config={config}
        setConfig={setConfig}
        isOpen={settingsOpen}
        onClose={() => setSettingsOpen(false)}
      />

      <TemplateModal
        selectedTemplate={templateId}
        customPrompt={customPrompt}
        onSelect={setTemplateId}
        onUpdateCustom={setCustomPrompt}
        isOpen={templateOpen}
        onClose={() => setTemplateOpen(false)}
      />
    </div>
  );
}
