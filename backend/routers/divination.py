"""
Divination router - handles divination requests and results.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from models.schemas import DivinationRequest, DivinationResult, Line, Hexagram
from utils.divination_logic import (
    generate_six_lines,
    get_hexagram_from_lines,
    get_changed_hexagram,
    generate_interpretation
)

router = APIRouter(prefix="/api", tags=["divination"])


@router.post("/divination", response_model=DivinationResult)
async def perform_divination(request: DivinationRequest) -> DivinationResult:
    """
    Perform a divination reading based on the provided question.
    
    Args:
        request: DivinationRequest containing the question
        
    Returns:
        DivinationResult: Complete divination result with hexagrams and interpretation
        
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
        
        # Generate detailed interpretation
        interpretation: str = generate_interpretation(
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
            "step3": "获得卦象和解释",
            "step4": "根据建议做出决策"
        },
        "tips": [
            "问题要具体明确，避免过于宽泛",
            "保持诚心诚意的态度",
            "理性对待占卜结果，仅供参考",
            "重要决策建议咨询专业人士"
        ],
        "example_questions": [
            "我的事业发展如何？",
            "这段感情能否长久？",
            "是否适合投资这个项目？",
            "如何改善与同事的关系？"
        ]
    }
