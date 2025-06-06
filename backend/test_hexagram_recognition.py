#!/usr/bin/env python3
"""
测试卦象识别和变爻系统的准确性
"""

import requests
import json
from typing import List, Dict, Any

API_BASE = "http://localhost:8000"

def test_manual_divination(lines: List[int], expected_original: int, expected_changed: int = None, description: str = ""):
    """
    测试手动占卜API
    
    Args:
        lines: 六爻数值列表 [第1爻, 第2爻, 第3爻, 第4爻, 第5爻, 第6爻]
        expected_original: 期望的主卦编号
        expected_changed: 期望的变卦编号（如果有变爻）
        description: 测试描述
    """
    payload = {
        "question": f"测试案例: {description}",
        "lines": lines,
        "birth_date": "1990-01-01"
    }
    
    try:
        response = requests.post(f"{API_BASE}/api/divination/manual", json=payload)
        response.raise_for_status()
        result = response.json()
        
        original_number = result["originalHexagram"]["number"]
        original_name = result["originalHexagram"]["chineseName"]
        
        print(f"\n测试: {description}")
        print(f"输入爻线: {lines}")
        print(f"主卦: 第{original_number}卦 {original_name}")
        
        # 检查变爻
        changing_lines = [line["position"] for line in result["lines"] if line["changing"]]
        if changing_lines:
            changed_number = result["changedHexagram"]["number"]
            changed_name = result["changedHexagram"]["chineseName"]
            print(f"变爻: 第{', '.join(map(str, changing_lines))}爻")
            print(f"变卦: 第{changed_number}卦 {changed_name}")
        else:
            print("无变爻")
        
        # 验证结果
        success = True
        if original_number != expected_original:
            print(f"❌ 主卦错误: 期望第{expected_original}卦，实际第{original_number}卦")
            success = False
        
        if expected_changed is not None:
            if not result["changedHexagram"]:
                print(f"❌ 变卦错误: 期望第{expected_changed}卦，实际无变卦")
                success = False
            elif result["changedHexagram"]["number"] != expected_changed:
                print(f"❌ 变卦错误: 期望第{expected_changed}卦，实际第{result['changedHexagram']['number']}卦")
                success = False
        
        if success:
            print("✅ 测试通过")
        
        return success
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

def main():
    """运行测试套件"""
    print("=" * 60)
    print("易经变爻识别系统测试")
    print("=" * 60)
    
    test_cases = [
        # 基础八卦测试
        {
            "lines": [7, 7, 7, 7, 7, 7],  # 全阳
            "expected_original": 1,  # 乾为天
            "description": "乾卦 - 全阳爻"
        },
        {
            "lines": [8, 8, 8, 8, 8, 8],  # 全阴
            "expected_original": 2,  # 坤为地
            "description": "坤卦 - 全阴爻"
        },
        
        # 风天小畜测试
        {
            "lines": [7, 7, 7, 8, 7, 7],  # 下乾上巽
            "expected_original": 9,  # 风天小畜
            "description": "风天小畜 - 第4爻阴"
        },
        
        # 变爻测试
        {
            "lines": [7, 7, 7, 6, 7, 7],  # 第4爻老阴（变爻）
            "expected_original": 9,  # 风天小畜
            "expected_changed": 1,   # 变卦：乾为天
            "description": "风天小畜第4爻变 → 乾为天"
        },
        {
            "lines": [7, 7, 7, 9, 7, 7],  # 第4爻老阳（变爻）
            "expected_original": 1,  # 乾为天
            "expected_changed": 9,   # 变卦：风天小畜
            "description": "乾为天第4爻变 → 风天小畜"
        },
        
        # 多变爻测试
        {
            "lines": [9, 7, 7, 6, 7, 7],  # 第1爻和第4爻变
            "expected_original": 9,  # 风天小畜
            "expected_changed": 2,   # 变卦：坤为地
            "description": "风天小畜第1、4爻变 → 坤为地"
        },
        
        # 天泽履测试
        {
            "lines": [7, 7, 7, 8, 7, 8],  # 下乾上兑
            "expected_original": 10,  # 天泽履
            "description": "天泽履 - 下乾上兑"
        },
    ]
    
    passed = 0
    total = len(test_cases)
    
    for test_case in test_cases:
        if test_manual_divination(**test_case):
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！变爻识别系统工作正常。")
    else:
        print(f"⚠️  {total - passed} 个测试失败，需要进一步调试。")

if __name__ == "__main__":
    main()
