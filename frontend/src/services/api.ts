// API配置和工具函数
const API_BASE_URL = import.meta.env.DEV ? '' : 'http://localhost:8000';

export const api = {
  // 检测API是否可用
  async checkApiHealth(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return response.ok;
    } catch (error) {
      console.error('API健康检查失败:', error);
      return false;
    }
  },
  // 执行占卜
  async performDivination(question: string, language: string = 'zh', includeNajia: boolean = false): Promise<any> {
    const url = `${API_BASE_URL}/api/divination?language=${language}&include_najia=${includeNajia}`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question: question.trim() }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`API请求失败 (${response.status}): ${errorText}`);
    }

    return await response.json();
  },

  // 手动占卜
  async performManualDivination(question: string, lines: number[], includeNajia: boolean = false, language: string = 'zh'): Promise<any> {
    const url = `${API_BASE_URL}/api/divination/manual?include_najia=${includeNajia}&language=${language}`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        question: question.trim(),
        lines: lines
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`手动占卜失败 (${response.status}): ${errorText}`);
    }

    return await response.json();
  },

  // 获取占卜帮助信息
  async getDivinationHelp(): Promise<any> {
    const url = `${API_BASE_URL}/api/divination/help`;
    
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`获取帮助信息失败 (${response.status}): ${errorText}`);
    }

    return await response.json();
  },

  // AI聊天
  async aiChat(message: string, hexagramContext: any, conversationHistory: any[]): Promise<any> {
    const url = `${API_BASE_URL}/api/divination/ai-chat`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message,
        hexagram_context: hexagramContext,
        conversation_history: conversationHistory
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`AI聊天失败 (${response.status}): ${errorText}`);
    }

    return await response.json();
  },

  // 纳甲六爻占卜
  async performNajiaDivination(question: string, hexagramData?: any): Promise<any> {
    const url = `${API_BASE_URL}/api/divination/najia`;
    
    const requestBody: any = { question: question.trim() };
    if (hexagramData) {
      requestBody.hexagram_data = hexagramData;
    }
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`纳甲占卜失败 (${response.status}): ${errorText}`);
    }

    return await response.json();
  }
};

export default api;