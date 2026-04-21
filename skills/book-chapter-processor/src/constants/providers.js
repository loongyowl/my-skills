export const PROVIDERS = [
  {
    id: 'deepseek',
    name: 'DeepSeek',
    baseUrl: 'https://api.deepseek.com/v1',
    model: 'deepseek-chat',
    supportsSystemPrompt: true
  },
  {
    id: 'openai',
    name: 'OpenAI',
    baseUrl: 'https://api.openai.com/v1',
    model: 'gpt-4o',
    supportsSystemPrompt: true
  },
  {
    id: 'anthropic',
    name: 'Anthropic (Claude)',
    baseUrl: 'https://api.anthropic.com/v1',
    model: 'claude-3-5-sonnet-20241022',
    supportsSystemPrompt: true,
    authHeader: 'x-api-key',
    apiVersion: '2023-06-01'
  },
  {
    id: 'google',
    name: 'Google (Gemini)',
    baseUrl: 'https://generativelanguage.googleapis.com/v1beta',
    model: 'gemini-1.5-pro',
    supportsSystemPrompt: true,
    specialFormat: 'google'
  },
  {
    id: 'custom',
    name: '自定义',
    baseUrl: '',
    model: '',
    supportsSystemPrompt: true
  }
];

export function getProviderById(id) {
  return PROVIDERS.find(p => p.id === id) || PROVIDERS[0];
}
