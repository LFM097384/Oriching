#!/usr/bin/env python3
"""
测试后端API是否正常工作
"""

import requests
import json
import sys

def test_backend_api():
    """测试后端API"""
    base_url = "http://localhost:8000"
    
    print("🔍 测试后端API连接...")
    
    # 1. 测试根路径
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ 根路径状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   服务信息: {data.get('message', 'N/A')}")
    except Exception as e:
        print(f"❌ 根路径连接失败: {e}")
        return False
    
    # 2. 测试健康检查
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ 健康检查状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   服务状态: {data.get('status', 'N/A')}")
    except Exception as e:
        print(f"❌ 健康检查失败: {e}")
    
    # 3. 测试占卜API（中文）
    try:
        divination_data = {
            "question": "测试问题：我的事业发展如何？"
        }
        response = requests.post(
            f"{base_url}/api/divination?language=zh",
            json=divination_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ 占卜API(中文)状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   原卦: {data.get('originalHexagram', {}).get('chineseName', 'N/A')}")
            print(f"   解释长度: {len(data.get('interpretation', ''))}")
        else:
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 占卜API(中文)失败: {e}")
    
    # 4. 测试占卜API（英文）
    try:
        divination_data = {
            "question": "Test question: How is my career development?"
        }
        response = requests.post(
            f"{base_url}/api/divination?language=en",
            json=divination_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ 占卜API(英文)状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   原卦: {data.get('originalHexagram', {}).get('name', 'N/A')}")
            print(f"   解释长度: {len(data.get('interpretation', ''))}")
        else:
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"❌ 占卜API(英文)失败: {e}")
    
    return True

if __name__ == "__main__":
    print("🚀 易经占卜后端API测试")
    print("=" * 50)
    
    success = test_backend_api()
    
    print("=" * 50)
    if success:
        print("✅ 后端API测试完成")
    else:
        print("❌ 后端API测试失败")
        sys.exit(1)
