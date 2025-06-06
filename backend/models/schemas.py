"""
Pydantic schemas for data validation and serialization.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
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
