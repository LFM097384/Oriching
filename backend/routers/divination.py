"""
Divination router - handles divination requests and results.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from models.schemas import (
    DivinationRequest, ManualDivinationRequest, DivinationResult, Line, Hexagram
)
from utils.divination_logic import (
    generate_six_lines,
    get_hexagram_from_lines,
    get_changed_hexagram,
    generate_interpretation,
    generate_najia_divination,
    generate_najia_interpretation
)
from utils.deepseek_ai import get_ai_interpretation, chat_with_ai
from typing import Optional

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
async def perform_divination(
    request: DivinationRequest, 
    language: Optional[str] = Query("zh", description="Language code: zh for Chinese, en for English"),
    include_najia: Optional[bool] = Query(False, description="Whether to include traditional najia analysis")
) -> DivinationResult:
    """
    Perform a divination reading based on the provided question.
    
    Args:
        request: DivinationRequest containing the question
        language: Language code for response (zh/en)
        include_najia: Whether to include traditional najia six-line analysis
        
    Returns:
        DivinationResult: Complete divination result with hexagrams and interpretation
        
    Raises:
        HTTPException: If the question is empty or invalid
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    try:
        # Set language for data manager
        from utils.divination_logic import set_language
        set_language(language)
        
        # Generate six lines using coin toss simulation
        lines: List[Line] = generate_six_lines()
        
        # Get the primary hexagram from the lines
        original_hexagram: Hexagram = get_hexagram_from_lines(lines)
        
        # Get the changed hexagram if there are changing lines
        changed_hexagram: Hexagram | None = get_changed_hexagram(lines)
        
        # Generate detailed interpretation using traditional method
        interpretation: str = generate_interpretation(
            request.question,
            original_hexagram,
            changed_hexagram,
            lines
        )
        
        # Add najia analysis if requested
        if include_najia:
            try:
                # Convert lines to najia format
                najia_params = []
                for line in lines:
                    if line.type == 'yang':
                        najia_params.append(1 if line.changing else 3)  # 老阳:1, 少阳:3                    else:
                        najia_params.append(4 if line.changing else 2)  # 老阴:4, 少阴:2
                
                # Generate najia analysis
                najia_result = generate_najia_divination(
                    params=najia_params,
                    question=request.question,
                    title=request.question,
                    date=datetime.now()
                )
                
                # Add najia interpretation to the main interpretation
                najia_interpretation = najia_result['najia_interpretation'] if najia_result else ''
                if najia_interpretation:
                    interpretation += f"\n\n{najia_interpretation}"
                
            except Exception as najia_error:
                # If najia analysis fails, continue with regular divination
                print(f"Najia analysis error: {najia_error}")
        
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
        "description": "基于传统易经理论的AI占卜系统，现已集成纳甲六爻分析",
        "usage": {
            "step1": "准备一个明确的问题",
            "step2": "调用 /api/divination 接口（自动起卦）或 /api/divination/manual 接口（手动输入）",
            "step3": "获得卦象和AI解释",
            "step4": "可选：添加 include_najia=true 参数获取传统纳甲分析",
            "step5": "使用 /api/divination/ai-chat 与AI深入讨论卦象含义",
            "step6": "根据建议做出决策"
        },
        "tips": [
            "问题要具体明确，避免过于宽泛",
            "保持诚心诚意的态度",
            "理性对待占卜结果，仅供参考",
            "重要决策建议咨询专业人士",
            "可以与AI助手深入讨论卦象含义",
            "纳甲分析提供更详细的传统六爻理论解读"
        ],
        "example_questions": [
            "我的事业发展如何？",
            "这段感情能否长久？",
            "是否适合投资这个项目？",
            "如何改善与同事的关系？"
        ],
        "features": {
            "basic_divination": [
                "自动起卦（三枚铜钱法模拟）",
                "手动输入爻象",
                "传统易经解卦",
                "变卦分析",
                "智能AI解读"
            ],
            "najia_analysis": [
                "完整的纳甲配置体系",
                "世应爻自动计算",
                "六亲关系分析（父母、兄弟、子孙、妻财、官鬼）",
                "六神配置（青龙、朱雀、勾陈、螣蛇、白虎、玄武）",
                "伏神计算",
                "变卦分析",
                "干支纪年",
                "旬空计算",
                "传统六爻占断要点"
            ]
        },
        "api_parameters": {
            "include_najia": "布尔值，是否包含纳甲分析。默认false，设为true时会在解释中添加传统纳甲六爻理论分析"
        },
        "line_values": {
            "6": "老阴（变爻）",
            "7": "少阳（静爻）", 
            "8": "少阴（静爻）",
            "9": "老阳（变爻）"
        },
        "ai_features": [
            "智能卦象解读",
            "个性化建议",
            "互动式问答",
            "深度分析指导",
            "纳甲理论解释"
        ]
    }


@router.post("/divination/manual", response_model=DivinationResult)
async def perform_manual_divination(
    request: ManualDivinationRequest,
    include_najia: Optional[bool] = Query(False, description="Whether to include traditional najia analysis")
) -> DivinationResult:
    """
    Perform a divination reading with manually provided lines.
    
    Args:
        request: ManualDivinationRequest containing question, lines, and optional birth date
        include_najia: Whether to include traditional najia six-line analysis
        
    Returns:
        DivinationResult: Complete divination result with hexagrams and interpretation
        
    Raises:
        HTTPException: If the question is empty, lines are invalid, or processing fails
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="问题不能为空")
    
    # Validate request has exactly 6 lines
    if len(request.lines) != 6:
        raise HTTPException(status_code=400, detail=f"必须提供6个爻，当前提供了{len(request.lines)}个")
    
    # Validate line values
    valid_line_values = {6, 7, 8, 9}
    for i, line_value in enumerate(request.lines):
        if line_value not in valid_line_values:
            raise HTTPException(
                status_code=400, 
                detail=f"第{i+1}爻的值无效: {line_value}。有效值为: 6(老阴), 7(少阳), 8(少阴), 9(老阳)"
            )
    
    try:
        # Convert numeric line values to Line objects
        lines: List[Line] = []
        for position, line_value in enumerate(request.lines, 1):
            line_type = 'yang' if line_value in [7, 9] else 'yin'
            changing = line_value in [6, 9]  # 老阴和老阳为变爻
            
            line = Line(
                position=position,
                type=line_type,
                changing=changing,
                text="",
                explanation=""
            )
            lines.append(line)
        
        # Get the primary hexagram from the lines
        original_hexagram: Hexagram = get_hexagram_from_lines(lines)
        
        # Get the changed hexagram if there are changing lines
        changed_hexagram: Hexagram | None = get_changed_hexagram(lines)
        
        # Generate detailed interpretation using traditional method
        interpretation: str = generate_interpretation(
            request.question,
            original_hexagram,
            changed_hexagram,
            lines
        )
        
        # Add najia analysis if requested
        if include_najia:
            try:
                # Convert request.lines directly to najia format
                najia_params = []
                for line_value in request.lines:
                    if line_value == 6:  # 老阴
                        najia_params.append(4)
                    elif line_value == 7:  # 少阳
                        najia_params.append(3)
                    elif line_value == 8:  # 少阴
                        najia_params.append(2)
                    elif line_value == 9:  # 老阳
                        najia_params.append(1)
                  # Generate najia analysis
                najia_result = generate_najia_divination(
                    params=najia_params,
                    question=request.question,
                    title=request.question,
                    date=datetime.now()
                )
                
                # Add najia interpretation to the main interpretation
                najia_interpretation = najia_result['najia_interpretation'] if najia_result else ''
                if najia_interpretation:
                    interpretation += f"\n\n{najia_interpretation}"
                
            except Exception as najia_error:
                # If najia analysis fails, continue with regular divination
                print(f"Najia analysis error: {najia_error}")
        
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


# 纳甲六爻请求模型
class NajiaRequest(BaseModel):
    question: str
    hexagram_data: Optional[Dict[str, Any]] = None

@router.post("/divination/najia")
async def najia_divination(request: NajiaRequest):
    """
    专门的纳甲六爻占卜端点
    
    Args:
        request: 包含问题和可选卦象数据的请求
        
    Returns:
        Dict: 纳甲六爻分析结果
    """
    try:
        # 如果提供了卦象数据，使用它；否则自动生成
        if request.hexagram_data and "lines" in request.hexagram_data:
            lines_data = request.hexagram_data["lines"]
            # 将数字转换为najia格式
            najia_params = []
            for line_value in lines_data:
                if line_value == 6:  # 老阴（变爻）
                    najia_params.append(4)
                elif line_value == 7:  # 少阳
                    najia_params.append(3)
                elif line_value == 8:  # 少阴
                    najia_params.append(2)
                elif line_value == 9:  # 老阳（变爻）
                    najia_params.append(1)
                else:
                    # 默认处理
                    najia_params.append(line_value % 4 + 1)
        else:
            # 自动生成六爻
            lines = generate_six_lines()
            najia_params = []
            for line in lines:
                if line.type == "yin":
                    najia_params.append(4 if line.changing else 2)  # 老阴:4, 少阴:2
                else:
                    najia_params.append(1 if line.changing else 3)  # 老阳:1, 少阳:3
        
        # 生成纳甲分析
        najia_result = generate_najia_divination(
            params=najia_params,
            question=request.question,
            title=request.question,
            date=datetime.now()
        )
          # 生成详细解释
        if najia_result:
            najia_interpretation = generate_najia_interpretation(najia_result['najia_result'], request.question)
            
            return {
                "question": request.question,
                "najia_analysis": najia_result,
                "interpretation": najia_interpretation,
                "timestamp": datetime.now().isoformat(),
                "method": "manual" if request.hexagram_data else "auto"
            }
        else:
            raise HTTPException(status_code=500, detail="纳甲分析生成失败")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"纳甲占卜服务出错: {str(e)}")


@router.post("/divination/consult")
async def basic_consult(request: DivinationRequest):
    """
    基础占卜咨询端点（兼容性）
    
    Args:
        request: 占卜请求
        
    Returns:
        Dict: 基础占卜结果
    """
    try:
        # 生成六爻
        lines = generate_six_lines()
          # 获取卦象
        hexagram = get_hexagram_from_lines(lines)
        if not hexagram:
            raise HTTPException(status_code=500, detail="无法识别卦象")
        
        # 获取变卦
        changed_hexagram = get_changed_hexagram(lines)
        
        # 生成解释
        interpretation = generate_interpretation(
            request.question,
            hexagram,
            changed_hexagram,
            lines
        )
        
        return {
            "question": request.question,
            "hexagram_name": hexagram.name if hexagram else "未知",
            "hexagram_number": hexagram.number if hexagram else 0,
            "interpretation": interpretation,            "lines": [{"position": i+1, "type": line.type, "changing": line.changing} 
                     for i, line in enumerate(lines)],
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"占卜服务出错: {str(e)}")
