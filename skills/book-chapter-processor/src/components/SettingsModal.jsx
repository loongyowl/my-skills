import { useState, useEffect } from 'react';
import { X, Eye, EyeOff, RefreshCw, Check } from 'lucide-react';
import { PROVIDERS, getProviderById } from '../constants/providers';
import { testConnection } from '../hooks/useLlm';

export default function SettingsModal({ config, setConfig, isOpen, onClose }) {
  const [localConfig, setLocalConfig] = useState(config);
  const [showApiKey, setShowApiKey] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  // 同步外部 config 变化到本地状态
  useEffect(() => {
    setLocalConfig(config);
  }, [config]);

  // ESC 键关闭，关闭时自动保存
  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        handleSave();
      }
    };

    const handleClickOutside = (e) => {
      if (e.target.classList.contains('modal-backdrop')) {
        handleSave();
      }
    };

    window.addEventListener('keydown', handleEscape);
    document.querySelectorAll('.modal-backdrop').forEach(el => {
      el.addEventListener('click', handleClickOutside);
    });

    return () => {
      window.removeEventListener('keydown', handleEscape);
      document.querySelectorAll('.modal-backdrop').forEach(el => {
        el.removeEventListener('click', handleClickOutside);
      });
    };
  }, [isOpen, localConfig]);

  if (!isOpen) return null;

  const handleProviderChange = (providerId) => {
    const provider = getProviderById(providerId);
    setLocalConfig({
      ...localConfig,
      provider: providerId,
      baseUrl: provider.baseUrl,
      model: provider.model
    });
    setTestResult(null);
  };

  const handleSave = () => {
    setConfig(localConfig);
    onClose();
  };

  const handleCancel = () => {
    setLocalConfig(config); // 恢复原始配置
    onClose();
  };

  const handleTest = async () => {
    setTesting(true);
    setTestResult(null);
    const result = await testConnection(localConfig);
    setTestResult(result);
    setTesting(false);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center modal-backdrop bg-black/40 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-lg mx-4 overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900">API 设置</h2>
          <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
            <X size={18} className="text-gray-500" />
          </button>
        </div>

        <div className="px-6 py-5 space-y-5">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">LLM 提供商</label>
            <select
              value={localConfig.provider}
              onChange={(e) => handleProviderChange(e.target.value)}
              className="w-full px-3 py-2.5 rounded-xl border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            >
              {PROVIDERS.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">API Key</label>
            <div className="relative">
              <input
                type={showApiKey ? 'text' : 'password'}
                value={localConfig.apiKey}
                onChange={(e) => { setLocalConfig({ ...localConfig, apiKey: e.target.value }); setTestResult(null); }}
                placeholder="sk-..."
                className="w-full px-3 py-2.5 pr-10 rounded-xl border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
              />
              <button
                onClick={() => setShowApiKey(!showApiKey)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                {showApiKey ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Base URL</label>
            <input
              type="text"
              value={localConfig.baseUrl}
              onChange={(e) => { setLocalConfig({ ...localConfig, baseUrl: e.target.value }); setTestResult(null); }}
              placeholder="https://api.example.com/v1"
              className="w-full px-3 py-2.5 rounded-xl border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">模型名称</label>
            <input
              type="text"
              value={localConfig.model}
              onChange={(e) => { setLocalConfig({ ...localConfig, model: e.target.value }); setTestResult(null); }}
              placeholder="gpt-4"
              className="w-full px-3 py-2.5 rounded-xl border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all"
            />
          </div>

          {testResult && (
            <div className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm ${testResult.success ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
              {testResult.success ? <Check size={16} /> : <X size={16} />}
              {testResult.message}
            </div>
          )}
        </div>

        <div className="flex items-center justify-between px-6 py-4 border-t border-gray-100 bg-gray-50/50">
          <button
            onClick={handleTest}
            disabled={testing || !localConfig.apiKey}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            <RefreshCw size={14} className={testing ? 'animate-spin' : ''} />
            {testing ? '测试中...' : '测试连接'}
          </button>
          <div className="flex gap-2">
            <button
              onClick={handleCancel}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-xl hover:bg-gray-50 transition-all"
            >
              取消
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 transition-all"
            >
              保存
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
