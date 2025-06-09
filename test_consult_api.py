#!/usr/bin/env python3
"""
Test the /divination/consult endpoint specifically
"""

import requests
import json

def test_consult_api():
    """Test the consult API endpoint"""
    url = "http://localhost:8000/api/divination/consult"
    
    test_data = {
        "question": "今天运势如何？"
    }
    
    try:
        print("🎯 测试基础占卜咨询 API...")
        print(f"URL: {url}")
        print(f"数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        
        response = requests.post(url, json=test_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 基础占卜咨询 API 成功!")
            print(f"问题: {result.get('question', '未知')}")
            print(f"卦象: {result.get('hexagram_name', '未知')}")
            print(f"卦号: {result.get('hexagram_number', '未知')}")
            print(f"解释长度: {len(result.get('interpretation', ''))}")
        else:
            print(f"❌ 基础占卜咨询 API 失败: {response.text}")
    except Exception as e:
        print(f"❌ 基础占卜咨询请求异常: {e}")

if __name__ == "__main__":
    test_consult_api()
