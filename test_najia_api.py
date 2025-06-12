#!/usr/bin/env python3
"""
测试纳甲API
"""
import requests
import json

def test_najia_api():
    url = "http://localhost:8000/api/divination/najia"
    
    payload = {
        "question": "测试纳甲功能是否正常"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        print("发送请求到:", url)
        print("请求数据:", json.dumps(payload, ensure_ascii=False, indent=2))
        
        response = requests.post(url, json=payload, headers=headers)
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n纳甲API测试成功!")
            print("返回数据结构:")
            
            # 检查重要字段
            if 'ganzhi_time' in result:
                print(f"✓ ganzhi_time: {result['ganzhi_time']}")
            else:
                print("✗ 缺少 ganzhi_time 字段")
                
            if 'original_hexagram' in result:
                print(f"✓ original_hexagram: {result['original_hexagram']['name']}")
            else:
                print("✗ 缺少 original_hexagram 字段")
                
            print(f"\n完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        else:
            print(f"请求失败: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("连接失败 - 确保后端服务正在运行")
    except Exception as e:
        print(f"测试出错: {e}")

if __name__ == "__main__":
    test_najia_api()
