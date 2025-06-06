#!/usr/bin/env python3
"""
直接测试变爻识别逻辑，不通过API
"""
import sys
import os

# 添加后端路径到Python路径
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

from models.schemas import Line
from utils.divination_logic import get_hexagram_from_lines, get_changed_hexagram

def test_changing_lines():
    print("=== 直接测试变爻识别逻辑 ===\n")
    
    # 测试案例1：[7,7,7,6,7,7] - 只有第4爻变
    print("测试1: [7,7,7,6,7,7] - 风天小畜，第4爻变")
    lines1 = [
        Line(position=1, type='yang', changing=False),  # 7 = 少阳
        Line(position=2, type='yang', changing=False),  # 7 = 少阳
        Line(position=3, type='yang', changing=False),  # 7 = 少阳
        Line(position=4, type='yin', changing=True),    # 6 = 老阴 (变爻)
        Line(position=5, type='yang', changing=False),  # 7 = 少阳
        Line(position=6, type='yang', changing=False),  # 7 = 少阳
    ]
    
    original1 = get_hexagram_from_lines(lines1)
    changed1 = get_changed_hexagram(lines1)
    
    print(f"主卦: {original1.chineseName} (#{original1.number})")
    changing_positions1 = [line.position for line in lines1 if line.changing]
    print(f"变爻: 第 {', '.join(map(str, changing_positions1))} 爻")
    if changed1:
        print(f"变卦: {changed1.chineseName} (#{changed1.number})")
    else:
        print("变卦: 无")
    print()
    
    # 测试案例2：[9,7,6,7,9,8] - 多个变爻
    print("测试2: [9,7,6,7,9,8] - 多个变爻")
    lines2 = [
        Line(position=1, type='yang', changing=True),   # 9 = 老阳 (变爻)
        Line(position=2, type='yang', changing=False),  # 7 = 少阳
        Line(position=3, type='yin', changing=True),    # 6 = 老阴 (变爻)
        Line(position=4, type='yang', changing=False),  # 7 = 少阳
        Line(position=5, type='yang', changing=True),   # 9 = 老阳 (变爻)
        Line(position=6, type='yin', changing=False),   # 8 = 少阴
    ]
    
    original2 = get_hexagram_from_lines(lines2)
    changed2 = get_changed_hexagram(lines2)
    
    print(f"主卦: {original2.chineseName} (#{original2.number})")
    changing_positions2 = [line.position for line in lines2 if line.changing]
    print(f"变爻: 第 {', '.join(map(str, changing_positions2))} 爻")
    if changed2:
        print(f"变卦: {changed2.chineseName} (#{changed2.number})")
        print("变爻详情:")
        for line in lines2:
            if line.changing:
                new_type = 'yin' if line.type == 'yang' else 'yang'
                print(f"  第{line.position}爻: {line.type} → {new_type}")
    else:
        print("变卦: 无")
    print()
    
    # 测试案例3：[7,8,7,8,7,8] - 无变爻
    print("测试3: [7,8,7,8,7,8] - 无变爻")
    lines3 = [
        Line(position=1, type='yang', changing=False),  # 7 = 少阳
        Line(position=2, type='yin', changing=False),   # 8 = 少阴
        Line(position=3, type='yang', changing=False),  # 7 = 少阳
        Line(position=4, type='yin', changing=False),   # 8 = 少阴
        Line(position=5, type='yang', changing=False),  # 7 = 少阳
        Line(position=6, type='yin', changing=False),   # 8 = 少阴
    ]
    
    original3 = get_hexagram_from_lines(lines3)
    changed3 = get_changed_hexagram(lines3)
    
    print(f"主卦: {original3.chineseName} (#{original3.number})")
    changing_positions3 = [line.position for line in lines3 if line.changing]
    if changing_positions3:
        print(f"变爻: 第 {', '.join(map(str, changing_positions3))} 爻")
    else:
        print("变爻: 无")
    if changed3:
        print(f"变卦: {changed3.chineseName} (#{changed3.number})")
    else:
        print("变卦: 无")

if __name__ == "__main__":
    test_changing_lines()
