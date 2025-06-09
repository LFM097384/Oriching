#!/usr/bin/env python3
"""
简单的连接测试
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_basic_connection():
    """测试基本连接"""
    print("🔍 测试基本连接...")
    
    # 测试根端点
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"根端点状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"响应内容: {response.json()}")
        else:
            print(f"响应内容: {response.text}")
    except Exception as e:
        print(f"根端点测试失败: {e}")
    
    # 测试文档端点
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=5)
        print(f"文档端点状态码: {response.status_code}")
    except Exception as e:
        print(f"文档端点测试失败: {e}")
    
    # 测试占卜端点
    try:
        response = requests.post(
            f"{BASE_URL}/api/divination",
            json={"question": "测试"},
            params={"language": "zh"},
            timeout=5
        )
        print(f"占卜端点状态码: {response.status_code}")
        if response.status_code == 200:
            print("占卜端点正常工作!")
        else:
            print(f"占卜端点响应: {response.text}")
    except Exception as e:
        print(f"占卜端点测试失败: {e}")

if __name__ == "__main__":
    test_basic_connection()
