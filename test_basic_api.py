#!/usr/bin/env python3
"""
测试基础占卜API的脚本
"""

import requests
import json

def test_basic_divination():
    """测试基础占卜API"""
    url = "http://localhost:8000/api/divination"
    data = {
        "question": "测试基础占卜API"
    }
    
    print("=== 测试基础占卜API ===")
    print(f"URL: {url}")
    print(f"数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(url, json=data, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API 调用成功!")
            print(f"问题: {result.get('question', 'N/A')}")
            print(f"原卦: {result.get('originalHexagram', {}).get('name', 'N/A')}")
            if result.get('changedHexagram'):
                print(f"变卦: {result['changedHexagram']['name']}")
            print(f"解释长度: {len(result.get('interpretation', ''))}")
        else:
            print("❌ API 调用失败!")
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

def test_basic_divination_with_najia():
    """测试包含纳甲分析的基础占卜API"""
    url = "http://localhost:8000/api/divination"
    data = {
        "question": "测试包含纳甲的基础占卜API"
    }
    params = {
        "include_najia": True
    }
    
    print("\n=== 测试基础占卜API（包含纳甲）===")
    print(f"URL: {url}")
    print(f"数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
    print(f"参数: {params}")
    
    try:
        response = requests.post(url, json=data, params=params, timeout=30)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API 调用成功!")
            print(f"问题: {result.get('question', 'N/A')}")
            print(f"原卦: {result.get('originalHexagram', {}).get('name', 'N/A')}")
            if result.get('changedHexagram'):
                print(f"变卦: {result['changedHexagram']['name']}")
            print(f"解释长度: {len(result.get('interpretation', ''))}")
            if "纳甲" in result.get('interpretation', ''):
                print("✅ 包含纳甲分析")
            else:
                print("⚠️ 未包含纳甲分析")
        else:
            print("❌ API 调用失败!")
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")

if __name__ == "__main__":
    test_basic_divination()
    test_basic_divination_with_najia()
