#!/usr/bin/env python3
"""
测试 API 端点的简单脚本
"""
import requests
import json

def test_najia_api():
    """测试纳甲六爻 API 端点"""
    url = "http://localhost:8000/api/divination/najia"
    
    # 测试数据
    test_data = {
        "question": "测试问题：工作是否顺利？",
        "hexagram_data": {
            "lines": [7, 8, 9, 6, 7, 8]
        }
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("🚀 发送 API 请求...")
        print(f"URL: {url}")
        print(f"数据: {json.dumps(test_data, ensure_ascii=False, indent=2)}")
        print("-" * 50)
        
        response = requests.post(url, json=test_data, headers=headers)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print("-" * 50)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API 调用成功!")
            print(f"响应数据长度: {len(str(result))} 字符")
            print("\n📊 纳甲六爻分析结果:")
            if 'interpretation' in result:
                print(result['interpretation'][:200] + "..." if len(result['interpretation']) > 200 else result['interpretation'])
            else:
                print(json.dumps(result, ensure_ascii=False, indent=2)[:500] + "...")
        else:
            print(f"❌ API 调用失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败: 无法连接到后端服务器")
        print("请确保后端服务正在运行在 http://localhost:8000")
    except Exception as e:
        print(f"❌ 请求异常: {e}")

def test_basic_divination_api():
    """测试基础占卜 API 端点"""
    url = "http://localhost:8000/api/divination/consult"
    
    test_data = {
        "question": "今天运势如何？"
    }
    
    try:
        print("\n🎯 测试基础占卜 API...")
        response = requests.post(url, json=test_data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ 基础占卜 API 成功!")
            print(f"卦象: {result.get('hexagram_name', '未知')}")
        else:
            print(f"❌ 基础占卜 API 失败: {response.text}")
    except Exception as e:
        print(f"❌ 基础占卜请求异常: {e}")

if __name__ == "__main__":
    print("=== I Ching API 测试 ===")
    test_najia_api()
    test_basic_divination_api()
    print("\n=== 测试完成 ===")