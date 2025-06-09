"""
Core divination logic for generating hexagrams and interpretations.
"""

import random
from typing import List, Literal, Tuple, Optional, Dict, Any
from datetime import datetime

from models.schemas import (
    Line, Hexagram, NajiaDivinationResult, NajiaHexagramInfo, 
    NajiaLineInfo, GanZhiTime, NajiaDivinationRequest
)

from .hexagram_data import HexagramDataManager
from .najia_oracle import NajiaOracle

# Initialize data manager
data_manager = HexagramDataManager()

def set_language(language: str) -> None:
    """
    Set the language for the data manager.
    
    Args:
        language: Language code ('zh' or 'en')
    """
    data_manager.set_language(language)

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


def generate_najia_divination(params: List[int] = None, question: str = "", 
                            gender: str = "", title: str = "", 
                            date = None) -> Dict[str, Any]:
    """
    生成完整的纳甲六爻排盘
    
    Args:
        params: 摇卦参数 [1-4] * 6，如果为None则随机生成
        question: 所问问题
        gender: 性别
        title: 测事标题
        date: 起卦时间
        
    Returns:
        完整的纳甲排盘结果
    """
    # 如果没有提供参数，随机生成
    if params is None:
        params = [random.randint(1, 4) for _ in range(6)]
    
    # 确保参数格式正确
    if len(params) != 6:
        params = params[:6] if len(params) > 6 else params + [2] * (6 - len(params))
    
    # 创建纳甲占卜器
    oracle = NajiaOracle(verbose=1)
    
    # 编译卦象
    oracle.compile(
        params=params,
        gender=gender,
        date=date,
        title=title,
        guaci=True
    )
    
    # 获取纳甲结果
    najia_result = oracle.get_najia_result()
    
    # 转换为标准爻线格式
    lines = []
    for i, param in enumerate(params):
        line_type = 'yang' if param in [1, 3] else 'yin'
        changing = param in [3, 4]  # 老阳老阴为动爻
        
        # 从纳甲结果获取详细信息
        line_info = najia_result['lines'][i] if i < len(najia_result['lines']) else {}
        
        lines.append(Line(
            position=i + 1,
            type=line_type,
            changing=changing,
            text=f"{line_info.get('najia', '')} {line_info.get('qin6', '')}",
            explanation=f"六神: {line_info.get('god6', '')}",
        ))
    
    # 获取原卦和变卦
    original_hexagram = get_hexagram_from_lines(lines)
    changed_hexagram = get_changed_hexagram(lines) if any(line.changing for line in lines) else None
    
    # 生成传统解释
    traditional_interpretation = generate_interpretation(question, original_hexagram, changed_hexagram, lines)
    
    # 添加纳甲专业解释
    najia_interpretation = generate_najia_interpretation(najia_result, question)
    
    return {
        'original_hexagram': original_hexagram,
        'changed_hexagram': changed_hexagram,
        'lines': lines,
        'najia_result': najia_result,
        'traditional_interpretation': traditional_interpretation,
        'najia_interpretation': najia_interpretation,
        'question': question,
        'params': params,
    }


def generate_najia_interpretation(najia_result: Dict[str, Any], question: str = "") -> str:
    """
    生成纳甲专业解释
    
    Args:
        najia_result: 纳甲排盘结果
        question: 所问问题
        
    Returns:
        纳甲解释文本
    """
    parts = []
    
    # 基本卦象信息
    original = najia_result.get('original_hexagram', {})
    parts.append("=== 纳甲六爻排盘 ===")
    parts.append(f"📊 主卦：{original.get('name', '未知卦')} ({original.get('gong', '未知')}宫)")
    
    gua_type = original.get('type', '')
    if gua_type:
        parts.append(f"🏷️ 卦性：{gua_type}")
    
    # 世应爻信息
    shiy = original.get('shiy', [])
    if len(shiy) >= 2:
        parts.append(f"🎯 世爻：第{shiy[0]}爻，应爻：第{shiy[1]}爻")
    
    # 变卦信息
    changed = najia_result.get('changed_hexagram')
    if changed:
        parts.append(f"🔄 变卦：{changed.get('name', '未知卦')} ({changed.get('gong', '未知')}宫)")
    
    parts.append("")
    
    # 六爻详细分析
    parts.append("=== 六爻分析 ===")
    lines = najia_result.get('lines', [])
    
    for i in range(5, -1, -1):  # 从上爻到初爻
        if i < len(lines):
            line = lines[i]
            parts.append(f"{'六' if i == 5 else '五四三二初'[i]}爻：{line.get('god6', '')} {line.get('qin6', '')} {line.get('najia', '')}")
            if line.get('changing'):
                parts.append(f"    ⚡ 动爻：此爻发动，主变化")
    
    parts.append("")
    
    # 六亲分析
    parts.append("=== 六亲关系 ===")
    qin6_list = [line.get('qin6', '') for line in lines]
    qin6_count = {}
    for qin in qin6_list:
        if qin:
            qin6_count[qin] = qin6_count.get(qin, 0) + 1
    
    for qin, count in qin6_count.items():
        if qin == '父母':
            parts.append(f"👨‍👩‍👧‍👦 {qin}：{count}个，主文书、房屋、长辈")
        elif qin == '兄弟':
            parts.append(f"👥 {qin}：{count}个，主朋友、同事、劫财")
        elif qin == '子孙':
            parts.append(f"👶 {qin}：{count}个，主晚辈、技艺、财源")
        elif qin == '妻财':
            parts.append(f"💰 {qin}：{count}个，主钱财、妻子、实用物品")
        elif qin == '官鬼':
            parts.append(f"👮‍♂️ {qin}：{count}个，主官府、疾病、鬼神、丈夫")
    
    # 伏神分析
    hidden = najia_result.get('hidden')
    if hidden:
        parts.append("")
        parts.append("=== 伏神分析 ===")
        parts.append(f"🫥 伏神卦：{hidden.get('name', '未知卦')}")
        parts.append("📍 缺失六亲通过伏神补充")
    
    # 时间信息
    lunar_info = najia_result.get('lunar_info', {})
    if lunar_info:
        parts.append("")
        parts.append("=== 时间信息 ===")
        gz = lunar_info.get('gz', {})
        parts.append(f"📅 四柱：{gz.get('year', '')}年 {gz.get('month', '')}月 {gz.get('day', '')}日 {gz.get('hour', '')}时")
        xkong = lunar_info.get('xkong', '')
        if xkong:
            parts.append(f"🕳️ 旬空：{xkong}")
    
    parts.append("")
    
    # 占卜建议
    parts.append("=== 占断要点 ===")
    
    # 根据用神分析
    if '妻财' in qin6_list and ('求财' in question or '钱' in question or '财' in question):
        parts.append("💡 求财以妻财为用神，观其旺衰动静")
    elif '官鬼' in qin6_list and ('工作' in question or '事业' in question or '官' in question):
        parts.append("💡 求官以官鬼为用神，观其旺衰动静")
    elif '子孙' in qin6_list and ('健康' in question or '病' in question):
        parts.append("💡 测病以子孙为用神，子孙发动病愈")
    elif '父母' in qin6_list and ('考试' in question or '学习' in question):
        parts.append("💡 求学以父母为用神，观其旺衰动静")
    
    # 动爻分析
    dong_yao = [i+1 for i, line in enumerate(lines) if line.get('changing')]
    if dong_yao:
        parts.append(f"⚡ 动爻：第{dong_yao}爻发动，主变化之应")
        if len(dong_yao) == 1:
            parts.append("📈 一爻动，事有专主")
        elif len(dong_yao) == 2:
            parts.append("⚖️ 二爻动，取两爻之应")
        elif len(dong_yao) >= 3:
            parts.append("🌀 多爻动，以变卦论之")
    else:
        parts.append("🔒 六爻皆静，以本卦论之")
    
    return "\n".join(parts)


def params_to_najia_format(params: List[int]) -> List[int]:
    """
    将通用参数转换为纳甲格式
    
    Args:
        params: 通用摇卦参数
        
    Returns:
        纳甲格式参数 [1-4]
    """
    if not params:
        return [random.randint(1, 4) for _ in range(6)]
    
    # 确保所有参数都在1-4范围内
    najia_params = []
    for p in params:
        if p == 0:
            najia_params.append(4)  # 0转换为老阴
        elif p in [1, 2, 3, 4]:
            najia_params.append(p)
        else:
            najia_params.append(p % 4 + 1)  # 其他值取模后映射到1-4
    
    return najia_params[:6] if len(najia_params) >= 6 else najia_params + [2] * (6 - len(najia_params))


def convert_najia_to_schema(najia_result: Dict[str, Any], question: str, 
                           divination_time: datetime = None) -> NajiaDivinationResult:
    """
    将纳甲结果转换为API schema格式
    
    Args:
        najia_result: 纳甲排盘结果
        question: 占卜问题
        divination_time: 起卦时间
        
    Returns:
        NajiaDivinationResult格式的结果
    """
    if divination_time is None:
        divination_time = datetime.now()
    
    # 提取lunar信息
    lunar_info = najia_result.get('lunar_info', {})
    gz = lunar_info.get('gz', {})
    
    # 构建干支时间
    ganzhi_time = GanZhiTime(
        year_gz=gz.get('year', ''),
        month_gz=gz.get('month', ''),
        day_gz=gz.get('day', ''),
        hour_gz=gz.get('hour', ''),
        xunkong=lunar_info.get('xkong', '').split(' ') if lunar_info.get('xkong') else []
    )
    
    # 构建六爻信息
    lines_info = []
    najia_lines = najia_result.get('lines', [])
    shiy = najia_result.get('shiy', [])
    
    for i in range(6):
        line_data = najia_lines[i] if i < len(najia_lines) else {}
        
        line_info = NajiaLineInfo(
            position=i + 1,
            yao_type='yang' if line_data.get('yao_type') == '阳' else 'yin',
            changing=line_data.get('changing', False),
            najia=line_data.get('najia', ''),
            wuxing=line_data.get('wuxing', ''),
            liuqin=line_data.get('qin6', ''),
            liushen=line_data.get('god6', ''),
            shi_yao=(i + 1) == shiy[0] if len(shiy) > 0 else False,
            ying_yao=(i + 1) == shiy[1] if len(shiy) > 1 else False,
            fushen=None,  # TODO: 从hidden信息中提取
            xunkong=line_data.get('xunkong', False)
        )
        lines_info.append(line_info)
    
    # 构建本卦信息
    original_hexagram = NajiaHexagramInfo(
        number=najia_result.get('number', 1),
        name=najia_result.get('name', ''),
        palace=najia_result.get('gong', ''),
        wuxing=najia_result.get('wuxing', ''),
        lines=lines_info,
        shi_yao_pos=shiy[0] if len(shiy) > 0 else 1,
        ying_yao_pos=shiy[1] if len(shiy) > 1 else 4
    )
    
    # 构建变卦信息（如果有）
    changed_hexagram = None
    bian = najia_result.get('bian')
    if bian:
        # TODO: 构建变卦的详细信息
        pass
    
    return NajiaDivinationResult(
        question=question,
        divination_time=divination_time,
        ganzhi_time=ganzhi_time,
        original_hexagram=original_hexagram,
        changed_hexagram=changed_hexagram,
        traditional_interpretation="",  # 将在API层设置
        detailed_analysis=najia_result
    )


def generate_najia_divination_for_api(question: str, 
                                     divination_time: datetime = None,
                                     manual_lines: List[int] = None) -> NajiaDivinationResult:
    """
    为API生成纳甲占卜结果
    
    Args:
        question: 占卜问题
        divination_time: 起卦时间
        manual_lines: 手动输入的爻象 [6,7,8,9]
        
    Returns:
        NajiaDivinationResult: API格式的纳甲占卜结果
    """
    if divination_time is None:
        divination_time = datetime.now()
    
    # 转换手动输入的爻象到纳甲格式
    if manual_lines:
        # 转换 6=老阴, 7=少阳, 8=少阴, 9=老阳 到纳甲格式 [1-4]
        params = []
        for line in manual_lines:
            if line == 6:  # 老阴
                params.append(4)
            elif line == 7:  # 少阳
                params.append(3)
            elif line == 8:  # 少阴
                params.append(2)
            elif line == 9:  # 老阳
                params.append(1)
            else:
                params.append(2)  # 默认少阴
    else:
        params = None
    
    # 生成纳甲排盘
    najia_result = generate_najia_divination(
        params=params,
        question=question,
        title=question,
        date=divination_time
    )
    
    # 转换为API schema格式
    return convert_najia_to_schema(
        najia_result['najia_result'],
        question,
        divination_time
    )
