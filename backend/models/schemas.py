"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any, List
from datetime import datetime


class TextExplanation(BaseModel):
    """基础文本解释结构"""
    text: str = Field(default="", description="原文")
    explanation: str = Field(default="", description="解释")


class LineInterpretations(BaseModel):
    """爻的各种解释"""
    shaoYong: Optional[Dict[str, Any]] = Field(default=None, description="邵雍河洛理数解释")
    fuPeiRong: Optional[Dict[str, Any]] = Field(default=None, description="傅佩榮解释")


class ChangeInfo(BaseModel):
    """变卦信息"""
    number: Optional[int] = Field(default=None, description="变卦编号")
    name: str = Field(default="", description="变卦名称")
    description: str = Field(default="", description="变卦描述")


class Line(BaseModel):
    """
    Represents a single line (yao) in a hexagram.
    """
    position: int = Field(..., ge=1, le=6, description="Line position from bottom to top")
    type: Literal['yang', 'yin'] = Field(..., description="Line type: yang (solid) or yin (broken)")
    changing: bool = Field(default=False, description="Whether this line is changing")
    text: str = Field(default="", description="爻辞原文")
    explanation: str = Field(default="", description="爻辞解释")
    image: TextExplanation = Field(default_factory=lambda: TextExplanation(), description="象辞")
    interpretations: LineInterpretations = Field(default_factory=lambda: LineInterpretations(), description="各种解释")
    changes_to: ChangeInfo = Field(default_factory=lambda: ChangeInfo(), description="变卦信息")

    model_config = {
        "json_schema_extra": {
            "example": {
                "position": 1,
                "type": "yang",
                "changing": False,
                "text": "初九。潜龙勿用。",
                "explanation": "初九在最下位，象征潜藏的龙，不宜有所行动。",
                "image": {
                    "text": "潜龙勿用，阳在下也。",
                    "explanation": "潜龙不宜使用，是因为阳气在下位的缘故。"
                }
            }
        }
    }


class HexagramInterpretations(BaseModel):
    """卦的各种解释"""
    shaoYong: Optional[Dict[str, Any]] = Field(default=None, description="邵雍河洛理数解卦")
    fuPeiRong: Optional[Dict[str, Any]] = Field(default=None, description="傅佩榮解卦手册")
    traditional: Optional[Dict[str, Any]] = Field(default=None, description="传统解卦")
    zhangMingRen: Optional[Dict[str, Any]] = Field(default=None, description="台湾张铭仁解卦")


class Hexagram(BaseModel):
    """
    Represents a complete hexagram with all its attributes.
    """
    number: int = Field(..., ge=1, le=64, description="Hexagram number")
    name: str = Field(..., description="卦名")
    chineseName: str = Field(..., description="中文完整名称")
    symbol: str = Field(default="", description="Unicode symbol")
    upperTrigram: str = Field(default="", description="上卦")
    lowerTrigram: str = Field(default="", description="下卦")
    kingWen: TextExplanation = Field(default_factory=lambda: TextExplanation(), description="卦辞")
    image: TextExplanation = Field(default_factory=lambda: TextExplanation(), description="象辞")
    interpretations: HexagramInterpretations = Field(default_factory=lambda: HexagramInterpretations(), description="各种解释")
    lines: list[Line] = Field(default_factory=list, description="六爻详细信息")
    # 添加与前端兼容的字段
    description: Optional[str] = Field(default=None, description="卦象描述（兼容字段）")
    fortune: Optional[str] = Field(default=None, description="运势解释（兼容字段）")
    love: Optional[str] = Field(default=None, description="感情解释（兼容字段）")
    career: Optional[str] = Field(default=None, description="事业解释（兼容字段）")
    health: Optional[str] = Field(default=None, description="健康解释（兼容字段）")
    advice: Optional[str] = Field(default=None, description="建议（兼容字段）")

    model_config = {
        "json_schema_extra": {
            "example": {
                "number": 1,
                "name": "乾卦",
                "chineseName": "乾為天",
                "symbol": "☰",
                "upperTrigram": "111",
                "lowerTrigram": "111",
                "kingWen": {
                    "text": "乾。元亨利貞。",
                    "explanation": "乾卦：大吉大利，吉利的貞卜。"
                },
                "image": {
                    "text": "天行健，君子以自強不息。",
                    "explanation": "天道剛健，運行不已。君子觀此卦象，從而以天為法，自強不息。"
                }
            }
        }
    }


class NajiaLineInfo(BaseModel):
    """纳甲爻信息"""
    position: int = Field(..., ge=1, le=6, description="爻位（1-6）")
    yao_type: Literal['yang', 'yin'] = Field(..., description="爻性：阳爻或阴爻")
    changing: bool = Field(default=False, description="是否变爻")
    najia: str = Field(default="", description="纳甲（天干地支）")
    wuxing: str = Field(default="", description="五行属性")
    liuqin: str = Field(default="", description="六亲关系")
    liushen: str = Field(default="", description="六神配置")
    shi_yao: bool = Field(default=False, description="是否世爻")
    ying_yao: bool = Field(default=False, description="是否应爻")
    fushen: Optional[str] = Field(default=None, description="伏神信息")
    xunkong: bool = Field(default=False, description="是否旬空")


class NajiaHexagramInfo(BaseModel):
    """纳甲卦象信息"""
    number: int = Field(..., ge=1, le=64, description="卦象编号")
    name: str = Field(..., description="卦名")
    palace: str = Field(..., description="卦宫归属")
    wuxing: str = Field(..., description="卦的五行属性")
    lines: List[NajiaLineInfo] = Field(..., min_length=6, max_length=6, description="六爻纳甲信息")
    shi_yao_pos: int = Field(..., ge=1, le=6, description="世爻位置")
    ying_yao_pos: int = Field(..., ge=1, le=6, description="应爻位置")


class GanZhiTime(BaseModel):
    """干支时间信息"""
    year_gz: str = Field(..., description="年干支")
    month_gz: str = Field(..., description="月干支")
    day_gz: str = Field(..., description="日干支")
    hour_gz: str = Field(..., description="时干支")
    xunkong: List[str] = Field(default_factory=list, description="旬空地支")


class DivinationRequest(BaseModel):
    """
    Request model for divination.
    """
    question: str = Field(..., min_length=1, max_length=500, description="The divination question")

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "我的事业发展如何？"
            }
        }
    }


class ManualDivinationRequest(BaseModel):
    """
    Request model for manual divination with provided lines.
    """
    question: str = Field(..., min_length=1, max_length=500, description="The divination question")
    lines: list[int] = Field(..., min_length=6, max_length=6, description="Six lines as numbers: 6=老阴, 7=少阳, 8=少阴, 9=老阳")
    birth_date: Optional[str] = Field(None, description="Birth date for personalized interpretation")

    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "测试变爻识别",
                "lines": [7, 7, 7, 6, 7, 7],
                "birth_date": "1990-01-01"
            }
        }
    }


class DivinationResult(BaseModel):
    """
    Complete divination result.
    """
    originalHexagram: Hexagram = Field(..., description="Primary hexagram")
    changedHexagram: Optional[Hexagram] = Field(None, description="Changed hexagram")
    lines: list[Line] = Field(..., min_length=6, max_length=6, description="Six lines of the hexagram")
    question: str = Field(..., description="Original question")
    timestamp: datetime = Field(..., description="Divination timestamp")
    interpretation: str = Field(..., description="Complete interpretation")


class HexagramResponse(BaseModel):
    """
    Response model for hexagram queries.
    """
    hexagrams: list[Hexagram] = Field(..., description="List of hexagrams")
    total: int = Field(..., description="Total number of hexagrams")


class NajiaDivinationRequest(BaseModel):
    """纳甲起卦请求"""
    question: str = Field(..., min_length=1, max_length=500, description="占卜问题")
    divination_time: Optional[datetime] = Field(default=None, description="起卦时间，不填则使用当前时间")
    manual_lines: Optional[List[int]] = Field(default=None, min_length=6, max_length=6, 
                                            description="手动输入爻象: 6=老阴, 7=少阳, 8=少阴, 9=老阳")


class NajiaDivinationResult(BaseModel):
    """纳甲占卜结果"""
    question: str = Field(..., description="占卜问题")
    divination_time: datetime = Field(..., description="起卦时间")
    ganzhi_time: GanZhiTime = Field(..., description="干支时间")
    original_hexagram: NajiaHexagramInfo = Field(..., description="本卦纳甲信息")
    changed_hexagram: Optional[NajiaHexagramInfo] = Field(default=None, description="变卦纳甲信息")
    traditional_interpretation: str = Field(..., description="传统纳甲解卦")
    detailed_analysis: Dict[str, Any] = Field(default_factory=dict, description="详细分析结果")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "question": "测试纳甲起卦",
                "divination_time": "2024-01-15T10:30:00",
                "ganzhi_time": {
                    "year_gz": "甲辰",
                    "month_gz": "丁丑", 
                    "day_gz": "癸巳",
                    "hour_gz": "丁巳",
                    "xunkong": ["戌", "亥"]
                },
                "traditional_interpretation": "传统纳甲解卦内容..."
            }
        }
    }
