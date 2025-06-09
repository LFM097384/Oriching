import os
import httpx
import json
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import asyncio
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepSeekAI:
    """DeepSeek AI服务类，用于易经占卜解读"""
    
    def __init__(self):
        self.api_key = os.getenv("DeepSeek_API_KEY")
        self.base_url = "https://api.deepseek.com/v1"
        self.model = "deepseek-chat"
        
        if not self.api_key:
            logger.error("DeepSeek API密钥未设置")
            raise ValueError("DeepSeek API密钥未找到，请在.env文件中设置DeepSeek_API_KEY")
    
    async def get_hexagram_interpretation(
        self, 
        question: str,
        original_hexagram: Dict[str, Any],
        changed_hexagram: Optional[Dict[str, Any]] = None,
        lines: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        获取卦象的AI解读
        
        Args:
            question: 用户的问题
            original_hexagram: 本卦信息
            changed_hexagram: 变卦信息（可选）
            lines: 爻的信息（可选）
        
        Returns:
            AI生成的解读文本
        """
        try:
            # 构建系统提示
            system_prompt = self._build_system_prompt()
            
            # 构建用户输入
            user_input = self._build_user_input(question, original_hexagram, changed_hexagram, lines)
            
            # 调用DeepSeek API
            response = await self._call_deepseek_api(system_prompt, user_input)
            
            return response
            
        except Exception as e:
            logger.error(f"AI解读生成失败: {e}")
            return self._get_fallback_interpretation(original_hexagram, changed_hexagram)
    
    async def chat_about_hexagram(
        self,
        user_message: str,
        hexagram_context: Dict[str, Any],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        """
        与AI进行关于卦象的对话
        
        Args:
            user_message: 用户消息
            hexagram_context: 卦象上下文信息
            conversation_history: 对话历史
        
        Returns:
            AI回复
        """
        try:
            # 构建对话系统提示
            system_prompt = self._build_chat_system_prompt(hexagram_context)
            
            # 构建消息历史
            messages = [{"role": "system", "content": system_prompt}]
            
            # 添加对话历史
            if conversation_history:
                messages.extend(conversation_history)
            
            # 添加当前用户消息
            messages.append({"role": "user", "content": user_message})
            
            # 调用API
            response = await self._call_deepseek_api_with_messages(messages)
            
            return response
            
        except Exception as e:
            logger.error(f"AI对话生成失败: {e}")
            return "抱歉，AI助手暂时无法回应。请稍后再试。"
    
    def _build_system_prompt(self) -> str:
        """构建系统提示"""
        return """你是一位精通《易经》的资深占卜师和智者，具有深厚的中国古代哲学素养。

你的特点：
1. 深谙易经六十四卦的含义、卦辞、象辞和爻辞
2. 能够结合现代生活情境给出实用的建议
3. 语言优雅而富有哲理，但不失实用性
4. 既尊重传统又与时俱进

请根据用户的问题和卦象信息，提供：
1. 卦象的基本含义解释
2. 针对具体问题的分析
3. 实际的建议和指导
4. 时机把握的建议

回答要求：
- 语言简洁明了，避免过于玄奥
- 结合现代生活实际
- 给出具体可行的建议
- 保持积极正面的态度
- 字数控制在300-500字"""

    def _build_chat_system_prompt(self, hexagram_context: Dict[str, Any]) -> str:
        """构建对话系统提示"""
        original_name = hexagram_context.get('originalHexagram', {}).get('chineseName', '未知')
        changed_name = hexagram_context.get('changedHexagram', {}).get('chineseName', '')
        question = hexagram_context.get('question', '')
        
        context_info = f"本次占卜的问题是：{question}\n本卦：{original_name}"
        if changed_name:
            context_info += f"\n变卦：{changed_name}"
        
        return f"""你是一位精通《易经》的AI助手，正在帮助用户解读占卜结果。

当前占卜情境：
{context_info}

你需要：
1. 基于这个卦象回答用户的问题
2. 提供深入的分析和建议
3. 回答要简洁实用，避免过于抽象
4. 保持耐心和智慧的语调
5. 每次回复控制在150字以内

请始终围绕这个卦象进行讨论，帮助用户更好地理解和应用占卜结果。"""
    
    def _build_user_input(
        self, 
        question: str,
        original_hexagram: Dict[str, Any],
        changed_hexagram: Optional[Dict[str, Any]] = None,
        lines: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """构建用户输入"""
        input_parts = [f"问题：{question}"]
        
        # 本卦信息
        original_name = original_hexagram.get('chineseName', '未知')
        input_parts.append(f"本卦：{original_name}")
        
        # 卦辞
        if 'kingWen' in original_hexagram:
            king_wen = original_hexagram['kingWen']
            input_parts.append(f"卦辞：{king_wen.get('text', '')}")
            if king_wen.get('explanation'):
                input_parts.append(f"卦辞释义：{king_wen.get('explanation')}")
        
        # 象辞
        if 'image' in original_hexagram:
            image = original_hexagram['image']
            input_parts.append(f"象辞：{image.get('text', '')}")
            if image.get('explanation'):
                input_parts.append(f"象辞释义：{image.get('explanation')}")
        
        # 变卦信息
        if changed_hexagram:
            changed_name = changed_hexagram.get('chineseName', '未知')
            input_parts.append(f"变卦：{changed_name}")
        
        # 变爻信息
        if lines:
            changing_lines = [line for line in lines if line.get('changing', False)]
            if changing_lines:
                input_parts.append(f"变爻：{len(changing_lines)}个")
                for line in changing_lines:
                    pos = line.get('position', 0)
                    text = line.get('text', '')
                    if text:
                        input_parts.append(f"第{pos}爻：{text}")
        
        input_parts.append("请针对以上问题和卦象给出详细的解读和建议。")
        
        return "\n".join(input_parts)
    
    async def _call_deepseek_api(self, system_prompt: str, user_input: str) -> str:
        """调用DeepSeek API"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
        
        return await self._call_deepseek_api_with_messages(messages)
    
    async def _call_deepseek_api_with_messages(self, messages: List[Dict[str, str]]) -> str:
        """使用消息列表调用DeepSeek API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"DeepSeek API错误: {response.status_code}, {response.text}")
                raise Exception(f"API调用失败: {response.status_code}")
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            return content.strip()
    
    def _get_fallback_interpretation(
        self, 
        original_hexagram: Dict[str, Any], 
        changed_hexagram: Optional[Dict[str, Any]] = None
    ) -> str:
        """获取后备解释（当AI服务不可用时）"""
        original_name = original_hexagram.get('chineseName', '未知卦象')
        
        fallback_text = f"根据{original_name}的卦象显示："
        
        # 简单的基于卦名的解读
        if '乾' in original_name:
            fallback_text += "这是一个积极进取的时机，宜刚健自强。"
        elif '坤' in original_name:
            fallback_text += "这是一个包容温和的时机，宜顺势而为。"
        elif '屯' in original_name:
            fallback_text += "当前处于起步阶段，需要耐心积累。"
        elif '蒙' in original_name:
            fallback_text += "需要学习和启蒙，宜虚心求教。"
        else:
            fallback_text += "需要综合考虑各种因素，谨慎行事。"
        
        if changed_hexagram:
            changed_name = changed_hexagram.get('chineseName', '')
            fallback_text += f"变为{changed_name}，表示情况会有所转变。"
        
        fallback_text += "建议结合自身实际情况，做出最适合的选择。"
        
        return fallback_text

# 创建全局实例
deepseek_ai = DeepSeekAI()

# 导出主要函数
async def get_ai_interpretation(question: str, original_hexagram: Dict, changed_hexagram: Optional[Dict] = None, lines: Optional[List] = None) -> str:
    """获取AI占卜解读"""
    return await deepseek_ai.get_hexagram_interpretation(question, original_hexagram, changed_hexagram, lines)

async def chat_with_ai(user_message: str, hexagram_context: Dict, conversation_history: List[Dict] = None) -> str:
    """与AI对话"""
    return await deepseek_ai.chat_about_hexagram(user_message, hexagram_context, conversation_history)
