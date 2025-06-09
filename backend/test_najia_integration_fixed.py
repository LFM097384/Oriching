#!/usr/bin/env python3
"""
Test script for najia integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime
from utils.divination_logic import generate_najia_divination_for_api, generate_najia_interpretation

def test_najia_divination():
    """Test najia divination functionality"""
    print("=== 测试纳甲六爻起卦功能 ===")
    
    # Test 1: Automatic divination
    print("\n1. 自动起卦测试:")
    try:
        result = generate_najia_divination_for_api(
            question="测试纳甲功能是否正常",
            divination_time=datetime.now()
        )
        
        print(f"问题: {result.question}")
        print(f"起卦时间: {result.divination_time}")
        print(f"干支时间: {result.ganzhi_time.year_gz}{result.ganzhi_time.month_gz}{result.ganzhi_time.day_gz}{result.ganzhi_time.hour_gz}")
        print(f"本卦: {result.original_hexagram.name} ({result.original_hexagram.palace}宫)")
        print(f"世爻位置: {result.original_hexagram.shi_yao_pos}")
        print(f"应爻位置: {result.original_hexagram.ying_yao_pos}")
        
        # Print line details
        print("\n六爻详情:")
        for line in result.original_hexagram.lines:
            shi_ying = ""
            if line.shi_yao:
                shi_ying = " [世]"
            elif line.ying_yao:
                shi_ying = " [应]"
            
            print(f"  {line.position}爻: {line.yao_type} {line.najia} {line.liuqin} {line.liushen}{shi_ying}")
            if line.xunkong:
                print(f"       (旬空)")
            if line.fushen:
                print(f"       伏神: {line.fushen}")
        
        if result.changed_hexagram:
            print(f"\n变卦: {result.changed_hexagram.name}")
        
        print("\n自动起卦测试 - ✅ 成功")
        
    except Exception as e:
        print(f"自动起卦测试 - ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 2: Manual lines
    print("\n2. 手动爻象测试:")
    try:
        manual_lines = [7, 8, 9, 6, 7, 8]  # 少阳、少阴、老阳(变)、老阴(变)、少阳、少阴
        result2 = generate_najia_divination_for_api(
            question="手动输入爻象测试",
            manual_lines=manual_lines
        )
        
        print(f"手动爻象: {manual_lines}")
        print(f"本卦: {result2.original_hexagram.name}")
        
        changing_lines = [line for line in result2.original_hexagram.lines if line.changing]
        if changing_lines:
            print(f"变爻: {[line.position for line in changing_lines]}")
        
        if result2.changed_hexagram:
            print(f"变卦: {result2.changed_hexagram.name}")
        
        print("手动爻象测试 - ✅ 成功")
        
    except Exception as e:
        print(f"手动爻象测试 - ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test 3: Generate interpretation
    print("\n3. 解卦测试:")
    try:
        interpretation = generate_najia_interpretation(result.detailed_analysis, result.question)
        print(f"解卦长度: {len(interpretation)} 字符")
        print(f"解卦摘要: {interpretation[:100]}...")
        print("解卦测试 - ✅ 成功")
        
    except Exception as e:
        print(f"解卦测试 - ❌ 失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_najia_divination()
