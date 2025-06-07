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
        lines: List of six Line objects (position 1-6, where 1 is bottom, 6 is top)
        
    Returns:
        Hexagram object matching the line pattern
        
    Raises:
        ValueError: If lines list is invalid
    """
    if len(lines) != 6:
        raise ValueError("必须提供6个爻")
    
    # 确保爻按位置排序（从下到上：1,2,3,4,5,6）
    sorted_lines = sorted(lines, key=lambda x: x.position)
      # 转换为二进制：上卦（第4,5,6爻）+ 下卦（第1,2,3爻）
    # 按照周易传统，所有三卦都从下往上数
    
    # 上卦：从第4爻到第6爻（从下往上）
    upper_trigram = ''.join([
        '1' if sorted_lines[3].type == 'yang' else '0',  # 第4爻（上卦底部）
        '1' if sorted_lines[4].type == 'yang' else '0',  # 第5爻（上卦中部）
        '1' if sorted_lines[5].type == 'yang' else '0'   # 第6爻（上卦顶部）
    ])
      # 下卦：从第1爻到第3爻（从下往上）
    lower_trigram = ''.join([
        '1' if sorted_lines[0].type == 'yang' else '0',  # 第1爻（下卦底部）
        '1' if sorted_lines[1].type == 'yang' else '0',  # 第2爻（下卦中部）
        '1' if sorted_lines[2].type == 'yang' else '0'   # 第3爻（下卦顶部）
    ])    # Find matching hexagram
    hexagram = data_manager.get_hexagram_by_trigrams(upper_trigram, lower_trigram)
    
    if hexagram is None:
        # Fallback to first hexagram if not found
        all_hexagrams = data_manager.get_all_hexagrams()
        if all_hexagrams:
            hexagram = all_hexagrams[0]
        else:
            raise ValueError("无法找到对应的卦象")
    
    # 重要：合并JSON中的爻辞信息到生成的爻线中，保持changing状态和position信息
    if hexagram.lines and len(hexagram.lines) == 6:
        # 创建新的爻线列表，保留changing状态但添加爻辞信息
        enhanced_lines = []
        for i, generated_line in enumerate(sorted_lines):
            json_line = hexagram.lines[i]
            # 创建增强的爻线，保留generated_line的changing状态，但添加JSON中的爻辞
            enhanced_line = Line(
                position=generated_line.position,
                type=generated_line.type,
                changing=generated_line.changing,
                text=json_line.text if hasattr(json_line, 'text') else None,
                explanation=json_line.explanation if hasattr(json_line, 'explanation') else None,
                image=json_line.image if hasattr(json_line, 'image') else None,
                interpretations=json_line.interpretations if hasattr(json_line, 'interpretations') else None
            )
            enhanced_lines.append(enhanced_line)
        
        hexagram.lines = enhanced_lines
    else:
        # 如果JSON中没有爻线信息，使用生成的爻线
        hexagram.lines = sorted_lines
    
    # 确保设置三爻信息
    hexagram.upperTrigram = upper_trigram
    hexagram.lowerTrigram = lower_trigram
    
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
      # Get the hexagram using the changed lines - this will properly merge line text data
    changed_hexagram = get_hexagram_from_lines(changed_lines)
    
    return changed_hexagram


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
      # Detailed interpretations - 详细解读
    interpretation_parts.append("== 详细解读 ==")
    
    # 卦象基本含义
    if hasattr(original_hexagram, 'interpretations') and original_hexagram.interpretations and hasattr(original_hexagram.interpretations, 'traditional'):
        if hasattr(original_hexagram.interpretations.traditional, 'description'):
            interpretation_parts.append(f"🔮 卦象释义：{original_hexagram.interpretations.traditional.description}")
    
    # 运势各方面解读
    if hasattr(original_hexagram, 'fortune') and original_hexagram.fortune:
        interpretation_parts.append(f"💰 总体运势：{original_hexagram.fortune}")
    
    if hasattr(original_hexagram, 'love') and original_hexagram.love:
        interpretation_parts.append(f"💕 感情婚姻：{original_hexagram.love}")
    
    if hasattr(original_hexagram, 'career') and original_hexagram.career:
        interpretation_parts.append(f"💼 事业工作：{original_hexagram.career}")
    
    if hasattr(original_hexagram, 'health') and original_hexagram.health:
        interpretation_parts.append(f"🏥 健康状况：{original_hexagram.health}")
    
    # 变爻解读
    changing_lines = [line for line in lines if line.changing]
    if changing_lines:
        interpretation_parts.append("")
        interpretation_parts.append("📍 变爻指导：")
        for line in changing_lines:
            if hasattr(line, 'explanation') and line.explanation:
                interpretation_parts.append(f"  第{line.position}爻：{line.explanation}")
    
    # 行动建议
    interpretation_parts.append("")
    if hasattr(original_hexagram, 'advice') and original_hexagram.advice:
        interpretation_parts.append(f"💡 行动建议：{original_hexagram.advice}")
        
    # Additional guidance based on changed hexagram
    if changed_hexagram:
        interpretation_parts.append("")
        interpretation_parts.append("== 变化趋势 ==")
        interpretation_parts.append(f"当前局势正在向【{changed_hexagram.chineseName}】的方向发展。")
        
        # 变卦详细解读
        if hasattr(changed_hexagram, 'interpretations') and changed_hexagram.interpretations and hasattr(changed_hexagram.interpretations, 'traditional'):
            if hasattr(changed_hexagram.interpretations.traditional, 'description'):
                interpretation_parts.append(f"🔄 变化含义：{changed_hexagram.interpretations.traditional.description}")
        
        # 变卦运势指向
        if hasattr(changed_hexagram, 'fortune') and changed_hexagram.fortune:
            interpretation_parts.append(f"📈 运势走向：{changed_hexagram.fortune}")
            
        if hasattr(changed_hexagram, 'advice') and changed_hexagram.advice:
            interpretation_parts.append(f"🎯 应对策略：{changed_hexagram.advice}")
            
        # 变化时机提示
        interpretation_parts.append(f"⏰ 变化提示：变爻显示变化正在发生，需要积极适应新的形势")
        
        interpretation_parts.append("")
    
    return "\n".join(interpretation_parts)
