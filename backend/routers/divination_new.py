"""
Divination router - handles divination requests and results with AI integration.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from models.schemas import DivinationRequest, ManualDivinationRequest, DivinationResult, Line, Hexagram
from utils.divination_logic import (
    generate_six_lines,
    get_hexagram_from_lines,
    get_changed_hexagram,
    generate_interpretation
)
from utils.deepseek_ai import get_ai_interpretation, chat_with_ai

router = APIRouter(prefix="/api", tags=["divination"])

# AI对话请求模型
class AIConversationRequest(BaseModel):
    message: str
    hexagram_context: Dict[str, Any]
    conversation_history: List[Dict[str, str]] = []

# AI对话响应模型
class AIConversationResponse(BaseModel):
    response: str
    timestamp: datetime


@router.post("/divination", response_model=DivinationResult)
async def perform_divination(request: DivinationRequest) -> DivinationResult:
    """
    Perform a divination reading based on the provided question with AI interpretation.
    
    Args:
        request: DivinationRequest containing the question
        
    Returns:
        DivinationResult: Complete divination result with hexagrams and AI interpretation
        
    Raises:
        HTTPException: If the question is empty or invalid
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    try:
        # Generate six lines using coin toss simulation
        lines: List[Line] = generate_six_lines()
        
        # Get the primary hexagram from the lines
        original_hexagram: Hexagram = get_hexagram_from_lines(lines)
        
        # Get the changed hexagram if there are changing lines
        changed_hexagram: Hexagram | None = get_changed_hexagram(lines)
        
        # Generate detailed interpretation using AI
        try:
            ai_interpretation = await get_ai_interpretation(
                request.question,
                original_hexagram.dict(),
                changed_hexagram.dict() if changed_hexagram else None,
                [line.dict() for line in lines]
            )
            interpretation = ai_interpretation
        except Exception as ai_error:
            print(f"AI解读失败，使用传统解读: {ai_error}")
            # Fallback to traditional interpretation
            interpretation = generate_interpretation(
                request.question,
                original_hexagram,
                changed_hexagram,
                lines
            )
        
        return DivinationResult(
            originalHexagram=original_hexagram,
            changedHexagram=changed_hexagram,
            lines=lines,
            question=request.question,
            timestamp=datetime.now(),
            interpretation=interpretation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"占卜过程中发生错误: {str(e)}")


@router.post("/divination/manual", response_model=DivinationResult)
async def perform_manual_divination(request: ManualDivinationRequest) -> DivinationResult:
    """
    Perform a divination reading with manually provided lines and AI interpretation.
    
    Args:
        request: ManualDivinationRequest containing question, lines, and optional birth date
        
    Returns:
        DivinationResult: Complete divination result with hexagrams and AI interpretation
        
    Raises:
        HTTPException: If the question is empty, lines are invalid, or processing fails
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    # Validate line values
    valid_values = {6, 7, 8, 9}
    if not all(line in valid_values for line in request.lines):
        raise HTTPException(
            status_code=400, 
            detail="爻值必须是6（老阴）、7（少阳）、8（少阴）或9（老阳）"
        )
    
    if len(request.lines) != 6:
        raise HTTPException(status_code=400, detail="必须提供6个爻值")
    
    try:
        # Convert manual input to Line objects
        lines: List[Line] = []
        for i, line_value in enumerate(request.lines):
            line_type = "yang" if line_value in [7, 9] else "yin"
            is_changing = line_value in [6, 9]
            
            line = Line(
                position=i + 1,
                type=line_type,
                changing=is_changing
            )
            lines.append(line)
        
        # Get the primary hexagram from the lines
        original_hexagram: Hexagram = get_hexagram_from_lines(lines)
        
        # Get the changed hexagram if there are changing lines
        changed_hexagram: Hexagram | None = get_changed_hexagram(lines)
        
        # Generate detailed interpretation using AI
        try:
            ai_interpretation = await get_ai_interpretation(
                request.question,
                original_hexagram.dict(),
                changed_hexagram.dict() if changed_hexagram else None,
                [line.dict() for line in lines]
            )
            interpretation = ai_interpretation
        except Exception as ai_error:
            print(f"AI解读失败，使用传统解读: {ai_error}")
            # Fallback to traditional interpretation
            interpretation = generate_interpretation(
                request.question,
                original_hexagram,
                changed_hexagram,
                lines
            )
        
        return DivinationResult(
            originalHexagram=original_hexagram,
            changedHexagram=changed_hexagram,
            lines=lines,
            question=request.question,
            timestamp=datetime.now(),
            interpretation=interpretation
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"手动占卜过程中发生错误: {str(e)}")


@router.post("/divination/ai-chat", response_model=AIConversationResponse)
async def chat_about_divination(request: AIConversationRequest) -> AIConversationResponse:
    """
    Chat with AI about a specific divination result.
    
    Args:
        request: AIConversationRequest containing user message and hexagram context
        
    Returns:
        AIConversationResponse: AI's response to the user's question
        
    Raises:
        HTTPException: If the message is empty or AI service fails
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    try:
        ai_response = await chat_with_ai(
            request.message,
            request.hexagram_context,
            request.conversation_history
        )
        
        return AIConversationResponse(
            response=ai_response,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI对话服务暂时不可用: {str(e)}")


@router.get("/divination/help")
async def get_divination_help() -> dict:
    """
    Get help information about how to use the divination API.
    
    Returns:
        dict: Help information and usage guidelines
    """
    return {
        "title": "易经占卜使用指南",
        "description": "基于传统易经理论的AI占卜系统",
        "usage": {
            "step1": "准备一个明确的问题",
            "step2": "调用 /api/divination 接口",
            "step3": "获得卦象和AI解释",
            "step4": "使用 /api/divination/ai-chat 与AI深入讨论",
            "step5": "根据建议做出决策"
        },
        "tips": [
            "问题要具体明确，避免过于宽泛",
            "保持诚心诚意的态度",
            "理性对待占卜结果，仅供参考",
            "重要决策建议咨询专业人士",
            "可以与AI助手深入讨论卦象含义"
        ],
        "example_questions": [
            "我的事业发展如何？",
            "这段感情能否长久？",
            "是否适合投资这个项目？",
            "如何改善与同事的关系？"
        ],
        "ai_features": [
            "智能卦象解读",
            "个性化建议",
            "互动式问答",
            "深度分析指导"
        ]
    }
