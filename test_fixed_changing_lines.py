#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的变爻识别功能
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from models.schemas import Line
from utils.divination_logic import get_hexagram_from_lines, get_changed_hexagram

def test_changing_lines_fixed():
    """测试修复后的变爻识别"""
    print("=== 测试修复后的变爻识别功能 ===\n")
    
    # 测试1: [7,7,7,6,7,7] - 風天小畜 #9，第4爻变
    print("测试1: [7,7,7,6,7,7]")
    lines1 = [
        Line(position=1, type='yang', changing=False),   # 7 少阳
        Line(position=2, type='yang', changing=False),   # 7 少阳  
        Line(position=3, type='yang', changing=False),   # 7 少阳
        Line(position=4, type='yin', changing=True),     # 6 老阴（变爻）
        Line(position=5, type='yang', changing=False),   # 7 少阳
        Line(position=6, type='yang', changing=False),   # 7 少阳
    ]
    
    original_hex1 = get_hexagram_from_lines(lines1)
    changed_hex1 = get_changed_hexagram(lines1)
    
    print(f"本卦: {original_hex1.chineseName} (#{original_hex1.number})")
    print(f"本卦爻线数量: {len(original_hex1.lines) if original_hex1.lines else 0}")
    if original_hex1.lines:
        changing_lines = [line.position for line in original_hex1.lines if line.changing]
        print(f"本卦变爻位置: {changing_lines}")
    
    if changed_hex1:
        print(f"变卦: {changed_hex1.chineseName} (#{changed_hex1.number})")
        print(f"变卦爻线数量: {len(changed_hex1.lines) if changed_hex1.lines else 0}")
        if changed_hex1.lines:
            print("变卦爻线详情:")
            for line in changed_hex1.lines:
                print(f"  第{line.position}爻: {line.type} (变爻: {line.changing})")
    else:
        print("无变卦")
    
    print()
    
    # 测试2: [9,7,6,7,9,8] - 多个变爻
    print("测试2: [9,7,6,7,9,8]")
    lines2 = [
        Line(position=1, type='yang', changing=True),    # 9 老阳（变爻）
        Line(position=2, type='yang', changing=False),   # 7 少阳
        Line(position=3, type='yin', changing=True),     # 6 老阴（变爻）
        Line(position=4, type='yang', changing=False),   # 7 少阳
        Line(position=5, type='yang', changing=True),    # 9 老阳（变爻）
        Line(position=6, type='yin', changing=False),    # 8 少阴
    ]
    
    original_hex2 = get_hexagram_from_lines(lines2)
    changed_hex2 = get_changed_hexagram(lines2)
    
    print(f"本卦: {original_hex2.chineseName} (#{original_hex2.number})")
    print(f"本卦爻线数量: {len(original_hex2.lines) if original_hex2.lines else 0}")
    if original_hex2.lines:
        changing_lines = [line.position for line in original_hex2.lines if line.changing]
        print(f"本卦变爻位置: {changing_lines}")
    
    if changed_hex2:
        print(f"变卦: {changed_hex2.chineseName} (#{changed_hex2.number})")
        print(f"变卦爻线数量: {len(changed_hex2.lines) if changed_hex2.lines else 0}")
        if changed_hex2.lines:
            print("变卦爻线详情:")
            for line in changed_hex2.lines:
                print(f"  第{line.position}爻: {line.type} (变爻: {line.changing})")
                
            # 验证变爻转换是否正确
            print("\n变爻转换验证:")
            for i, (orig_line, changed_line) in enumerate(zip(original_hex2.lines, changed_hex2.lines)):
                if orig_line.changing:
                    expected_type = 'yin' if orig_line.type == 'yang' else 'yang'
                    is_correct = changed_line.type == expected_type
                    print(f"  第{orig_line.position}爻: {orig_line.type} → {changed_line.type} {'✓' if is_correct else '✗'}")
    else:
        print("无变卦")

if __name__ == "__main__":
    test_changing_lines_fixed()
