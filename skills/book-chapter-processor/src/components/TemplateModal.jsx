import { X, Check, FileText } from 'lucide-react';
import { TEMPLATES } from '../constants/prompts';

export default function TemplateModal({ selectedTemplate, customPrompt, onSelect, onUpdateCustom, isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100">
          <h2 className="text-lg font-semibold text-gray-900">选择提示词模板</h2>
          <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-gray-100 transition-colors">
            <X size={18} className="text-gray-500" />
          </button>
        </div>

        <div className="px-6 py-5">
          <div className="grid gap-3 mb-5">
            {TEMPLATES.map(template => (
              <button
                key={template.id}
                onClick={() => { onSelect(template.id); onClose(); }}
                className={`flex items-start gap-3 p-4 rounded-xl border-2 text-left transition-all ${
                  selectedTemplate === template.id
                    ? 'border-indigo-500 bg-indigo-50/50'
                    : 'border-gray-100 hover:border-gray-200 hover:bg-gray-50'
                }`}
              >
                <div className={`mt-0.5 p-2 rounded-lg ${selectedTemplate === template.id ? 'bg-indigo-100 text-indigo-600' : 'bg-gray-100 text-gray-500'}`}>
                  <FileText size={16} />
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-medium text-gray-900">{template.name}</span>
                    {selectedTemplate === template.id && (
                      <Check size={14} className="text-indigo-600" />
                    )}
                  </div>
                  <p className="text-sm text-gray-500 mt-0.5">{template.description}</p>
                </div>
              </button>
            ))}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">自定义提示词（可选）</label>
            <textarea
              value={customPrompt}
              onChange={(e) => onUpdateCustom(e.target.value)}
              placeholder="输入自定义提示词来覆盖预设模板..."
              rows={4}
              className="w-full px-3 py-2.5 rounded-xl border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
            />
            <p className="text-xs text-gray-400 mt-1.5">留空则使用预设模板，填写后将覆盖预设</p>
          </div>
        </div>

        <div className="flex justify-end px-6 py-4 border-t border-gray-100 bg-gray-50/50">
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-xl hover:bg-indigo-700 transition-all"
          >
            完成
          </button>
        </div>
      </div>
    </div>
  );
}
