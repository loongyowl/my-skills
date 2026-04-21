import { getProviderById } from '../constants/providers';

// 请求超时时间（毫秒）
const REQUEST_TIMEOUT = 120000; // 2分钟

// 带超时的 fetch
async function fetchWithTimeout(url, options, timeout = REQUEST_TIMEOUT) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

export async function processWithLLM({
  config,
  systemPrompt,
  userContent,
  metadata,
  onProgress
}) {
  const { provider: providerId, apiKey, baseUrl, model } = config;
  const provider = getProviderById(providerId);

  const finalBaseUrl = baseUrl || provider.baseUrl;
  const finalModel = model || provider.model;

  const fullSystemPrompt = `${systemPrompt}

当前处理的书籍信息：
- 书名：${metadata.bookName || '未知'}
- 作者：${metadata.author || '未知'}
- 章节：${metadata.chapterName || '未知'}

请根据以上信息处理以下内容：`;

  const messages = [
    { role: 'system', content: fullSystemPrompt },
    { role: 'user', content: userContent }
  ];

  if (onProgress) onProgress({ status: 'connecting', message: '正在连接 API...' });

  try {
    if (provider.id === 'anthropic') {
      return await callAnthropicAPI({
        baseUrl: finalBaseUrl,
        apiKey,
        model: finalModel,
        messages,
        onProgress,
        apiVersion: provider.apiVersion
      });
    } else if (provider.id === 'google') {
      return await callGoogleAPI({
        baseUrl: finalBaseUrl,
        apiKey,
        model: finalModel,
        messages,
        onProgress
      });
    } else {
      return await callOpenAICompatibleAPI({
        baseUrl: finalBaseUrl,
        apiKey,
        model: finalModel,
        messages,
        onProgress
      });
    }
  } catch (error) {
    throw new Error(`API 调用失败: ${error.message}`);
  }
}

async function callOpenAICompatibleAPI({ baseUrl, apiKey, model, messages, onProgress }) {
  if (onProgress) onProgress({ status: 'processing', message: '正在处理（请耐心等待）...' });

  try {
    const response = await fetchWithTimeout(`${baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify({
        model,
        messages,
        temperature: 0.7,
        max_tokens: 8192
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return data.choices[0]?.message?.content || '';
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('请求超时（2分钟），请检查网络或减少文本长度');
    }
    throw error;
  }
}

async function callAnthropicAPI({ baseUrl, apiKey, model, messages, onProgress, apiVersion }) {
  if (onProgress) onProgress({ status: 'processing', message: '正在处理（请耐心等待）...' });

  const systemMessage = messages.find(m => m.role === 'system');
  const userMessages = messages.filter(m => m.role !== 'system');

  try {
    const response = await fetchWithTimeout(`${baseUrl}/messages`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': apiKey,
        'anthropic-version': apiVersion || '2023-06-01'
      },
      body: JSON.stringify({
        model,
        max_tokens: 8192,
        system: systemMessage?.content || '',
        messages: userMessages.map(m => ({
          role: m.role,
          content: m.content
        }))
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return data.content?.[0]?.text || '';
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('请求超时（2分钟），请检查网络或减少文本长度');
    }
    throw error;
  }
}

async function callGoogleAPI({ baseUrl, apiKey, model, messages, onProgress }) {
  if (onProgress) onProgress({ status: 'processing', message: '正在处理（请耐心等待）...' });

  const systemMessage = messages.find(m => m.role === 'system');
  const userMessage = messages.find(m => m.role === 'user');

  const url = `${baseUrl}/models/${model}:generateContent?key=${apiKey}`;

  try {
    const response = await fetchWithTimeout(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [{
          parts: [{ text: userMessage?.content || '' }]
        }],
        systemInstruction: {
          parts: [{ text: systemMessage?.content || '' }]
        },
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 8192
        }
      })
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.error?.message || `HTTP ${response.status}`);
    }

    const data = await response.json();
    return data.candidates?.[0]?.content?.parts?.[0]?.text || '';
  } catch (error) {
    if (error.name === 'AbortError') {
      throw new Error('请求超时（2分钟），请检查网络或减少文本长度');
    }
    throw error;
  }
}

export async function testConnection(config) {
  try {
    await processWithLLM({
      config,
      systemPrompt: '你是一个测试助手。请回复"连接成功"四个字。',
      userContent: '测试连接',
      metadata: { bookName: '测试', author: '测试', chapterName: '测试' }
    });
    return { success: true, message: '连接成功' };
  } catch (error) {
    return { success: false, message: error.message };
  }
}
