"""
Core divination logic for generating hexagrams and interpretations.
"""

import random
from typing import List, Literal, Tuple, Optional

from models.schemas import Line, Hexagram
from .hexagram_data import HexagramDataManager

# Initialize data manager
data_manager = HexagramDataManager()

LineType = Literal['oldYin', 'youngYang', 'youngYin', 'oldYang']


def throw_coins() -> Tuple[List[str], LineType, int]:
    """
    Simulate throwing three coins to determine a line type.
    
    In traditional I Ching divination, three coins are thrown:
    - Heads = 3, Tails = 2
    - Sum determines line type:
      - 6 (TTT): Old Yin (changing)
      - 7 (HTT, THT, TTH): Young Yang
      - 8 (HHT, HTH, THH): Young Yin  
      - 9 (HHH): Old Yang (changing)
    
    Returns:
        Tuple containing:
        - List of coin results ('heads' or 'tails')
        - Line type ('oldYin', 'youngYang', 'youngYin', 'oldYang')
        - Numeric value (6, 7, 8, or 9)
    """
    coins: List[str] = []
    heads_count = 0
    
    # Throw three coins
    for _ in range(3):
        coin = random.choice(['heads', 'tails'])
        coins.append(coin)
        if coin == 'heads':
            heads_count += 1
    
    # Determine line type based on heads count
    if heads_count == 0:  # TTT
        line_type: LineType = 'oldYin'
        line_value = 6
    elif heads_count == 1:  # HTT, THT, TTH
        line_type = 'youngYang'
        line_value = 7
    elif heads_count == 2:  # HHT, HTH, THH
        line_type = 'youngYin'
        line_value = 8
    else:  # HHH
        line_type = 'oldYang'
        line_value = 9
    
    return coins, line_type, line_value


def line_type_to_binary(line_type: LineType) -> str:
    """
    Convert line type to binary representation.
    
    Args:
        line_type: The type of line from coin toss
        
    Returns:
        '1' for yang lines, '0' for yin lines
    """
    return '1' if line_type in ['youngYang', 'oldYang'] else '0'


def is_changing_line(line_type: LineType) -> bool:
    """
    Check if a line is a changing line (old yang or old yin).
    
    Args:
        line_type: The type of line from coin toss
        
    Returns:
        True if the line is changing (old yang/yin), False otherwise
    """
    return line_type in ['oldYang', 'oldYin']


def generate_six_lines() -> List[Line]:
    """
    Generate six lines by throwing coins six times.
    
    Returns:
        List of six Line objects representing the hexagram
    """
    lines: List[Line] = []
    
    for position in range(1, 7):
        coins, line_type, line_value = throw_coins()
        
        # Convert to yang/yin representation
        type_str: Literal['yang', 'yin'] = 'yang' if line_type_to_binary(line_type) == '1' else 'yin'
        changing = is_changing_line(line_type)
        
        lines.append(Line(
            position=position,
            type=type_str,
            changing=changing
        ))
    
    return lines


def get_hexagram_from_lines(lines: List[Line]) -> Hexagram:
    """
    Get the hexagram corresponding to the given lines.
    
    Args:
        lines: List of six Line objects
        
    Returns:
        Hexagram object matching the line pattern
        
    Raises:
        ValueError: If lines list is invalid
    """
    if len(lines) != 6:
        raise ValueError("必须提供6个爻")
    
    # Convert lines to binary string (from bottom to top, so reverse order)
    binary_string = ''.join([
        '1' if line.type == 'yang' else '0' 
        for line in reversed(lines)
    ])
    
    # Split into upper and lower trigrams
    upper_trigram = binary_string[:3]
    lower_trigram = binary_string[3:6]
    
    # Find matching hexagram
    hexagram = data_manager.get_hexagram_by_trigrams(upper_trigram, lower_trigram)
    
    if hexagram is None:
        # Fallback to first hexagram if not found
        all_hexagrams = data_manager.get_all_hexagrams()
        if all_hexagrams:
            hexagram = all_hexagrams[0]
        else:
            raise ValueError("无法找到对应的卦象")
    
    return hexagram


def get_changed_hexagram(lines: List[Line]) -> Optional[Hexagram]:
    """
    Generate the changed hexagram if there are changing lines.
    
    Args:
        lines: List of six Line objects from original hexagram
        
    Returns:
        Changed hexagram if changing lines exist, None otherwise
    """
    # Check if there are any changing lines
    has_changing_lines = any(line.changing for line in lines)
    
    if not has_changing_lines:
        return None
    
    # Create changed lines by flipping changing lines
    changed_lines: List[Line] = []
    for line in lines:
        if line.changing:
            # Flip the line type
            new_type: Literal['yang', 'yin'] = 'yin' if line.type == 'yang' else 'yang'
        else:
            new_type = line.type
        
        changed_lines.append(Line(
            position=line.position,
            type=new_type,
            changing=False  # Changed lines are no longer changing
        ))
    
    return get_hexagram_from_lines(changed_lines)


def generate_interpretation(
    question: str,
    original_hexagram: Hexagram,
    changed_hexagram: Optional[Hexagram],
    lines: List[Line]
) -> str:
    """
    Generate a comprehensive interpretation of the divination result.
    
    Args:
        question: The original question asked
        original_hexagram: The primary hexagram
        changed_hexagram: The changed hexagram (if any)
        lines: The six lines with changing information
        
    Returns:
        Formatted interpretation string
    """
    interpretation_parts: List[str] = []
    
    # Question and basic info
    interpretation_parts.append(f"您的问题是：{question}")
    interpretation_parts.append("")
    
    # Original hexagram
    interpretation_parts.append(f"主卦：{original_hexagram.chineseName}（{original_hexagram.name}）")
    interpretation_parts.append(f"卦象：{original_hexagram.symbol}")
    
    # 获取卦象描述（兼容不同数据结构）
    original_description = ""
    if hasattr(original_hexagram, 'description') and original_hexagram.description:
        original_description = original_hexagram.description
    elif hasattr(original_hexagram, 'interpretations') and original_hexagram.interpretations:
        if original_hexagram.interpretations.traditional and hasattr(original_hexagram.interpretations.traditional, 'description'):
            original_description = original_hexagram.interpretations.traditional.description
    elif hasattr(original_hexagram, 'kingWen') and original_hexagram.kingWen:
        original_description = original_hexagram.kingWen.explanation

    interpretation_parts.append(f"解释：{original_description}")
    interpretation_parts.append("")
    
    # Changed hexagram if exists
    if changed_hexagram:
        changing_positions = [line.position for line in lines if line.changing]
        interpretation_parts.append(f"变卦：{changed_hexagram.chineseName}（{changed_hexagram.name}）")
        interpretation_parts.append(f"变爻：第 {', '.join(map(str, changing_positions))} 爻")
        
        # 获取变卦描述（兼容不同数据结构）
        changed_description = ""
        if hasattr(changed_hexagram, 'description') and changed_hexagram.description:
            changed_description = changed_hexagram.description
        elif hasattr(changed_hexagram, 'interpretations') and changed_hexagram.interpretations:
            if changed_hexagram.interpretations.traditional and hasattr(changed_hexagram.interpretations.traditional, 'description'):
                changed_description = changed_hexagram.interpretations.traditional.description
        elif hasattr(changed_hexagram, 'kingWen') and changed_hexagram.kingWen:
            changed_description = changed_hexagram.kingWen.explanation
            
        interpretation_parts.append(f"变卦解释：{changed_description}")
        interpretation_parts.append("")
    
    # Detailed interpretations - 仅在属性存在时添加
    interpretation_parts.append("== 详细解读 ==")
    
    if hasattr(original_hexagram, 'fortune') and original_hexagram.fortune:
        interpretation_parts.append(f"💰 运势：{original_hexagram.fortune}")
    
    if hasattr(original_hexagram, 'love') and original_hexagram.love:
        interpretation_parts.append(f"💕 感情：{original_hexagram.love}")
    
    if hasattr(original_hexagram, 'career') and original_hexagram.career:
        interpretation_parts.append(f"💼 事业：{original_hexagram.career}")
    
    if hasattr(original_hexagram, 'health') and original_hexagram.health:
        interpretation_parts.append(f"🏥 健康：{original_hexagram.health}")
    
    interpretation_parts.append("")
    
    # Advice - 仅在属性存在时添加
    if hasattr(original_hexagram, 'advice') and original_hexagram.advice:
        interpretation_parts.append(f"💡 建议：{original_hexagram.advice}")
        interpretation_parts.append("")
    
    # Additional guidance based on changed hexagram
    if changed_hexagram:
        interpretation_parts.append("== 变化趋势 ==")
        interpretation_parts.append(f"当前局势正在向 {changed_hexagram.chineseName} 的方向发展。")
        
        if hasattr(changed_hexagram, 'advice') and changed_hexagram.advice:
            interpretation_parts.append(f"变化建议：{changed_hexagram.advice}")
        
        interpretation_parts.append("")
    
    # Disclaimer
    interpretation_parts.append("== 温馨提示 ==")
    interpretation_parts.append("此占卜结果仅供参考，请结合实际情况理性判断。")
    interpretation_parts.append("重要决策建议咨询相关专业人士。")
    
    return "\n".join(interpretation_parts)
