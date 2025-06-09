#!/usr/bin/env python3
"""
测试语言切换功能
验证前端语言切换时后端是否正确返回对应语言的卦象数据
"""

import requests
import json
import time

# API基础URL
BASE_URL = "http://localhost:8000"

def test_language_switching():
    """测试语言切换功能"""
    print("🧪 开始测试语言切换功能...")
    
    # 测试问题
    test_question = "我的未来发展如何？"
    
    # 测试中文API
    print("\n📝 测试中文API...")
    try:
        response_zh = requests.post(
            f"{BASE_URL}/api/divination",
            json={"question": test_question},
            params={"language": "zh"}
        )
        
        if response_zh.status_code == 200:
            data_zh = response_zh.json()
            print(f"✅ 中文API调用成功")
            print(f"   卦象名称: {data_zh['originalHexagram']['chineseName']}")
            print(f"   卦象解释: {data_zh['interpretation'][:100]}...")
        else:
            print(f"❌ 中文API调用失败: {response_zh.status_code}")
            print(f"   错误信息: {response_zh.text}")
            
    except Exception as e:
        print(f"❌ 中文API调用异常: {e}")
    
    time.sleep(1)  # 短暂延迟
    
    # 测试英文API
    print("\n📝 测试英文API...")
    try:
        response_en = requests.post(
            f"{BASE_URL}/api/divination",
            json={"question": test_question},
            params={"language": "en"}
        )
        
        if response_en.status_code == 200:
            data_en = response_en.json()
            print(f"✅ 英文API调用成功")
            print(f"   卦象名称: {data_en['originalHexagram']['chineseName']}")
            print(f"   卦象解释: {data_en['interpretation'][:100]}...")
        else:
            print(f"❌ 英文API调用失败: {response_en.status_code}")
            print(f"   错误信息: {response_en.text}")
            
    except Exception as e:
        print(f"❌ 英文API调用异常: {e}")
    
    # 比较结果
    print("\n🔍 比较结果...")
    try:
        if 'data_zh' in locals() and 'data_en' in locals():
            # 检查是否使用了不同的数据源
            zh_name = data_zh['originalHexagram']['chineseName']
            en_name = data_en['originalHexagram']['chineseName']
            
            print(f"   中文卦象名称: {zh_name}")
            print(f"   英文卦象名称: {en_name}")
            
            # 检查名称格式差异（中文应该是纯中文，英文应该包含英文）
            if zh_name != en_name:
                print("✅ 语言切换功能正常 - 返回了不同语言的数据")
            else:
                print("⚠️  可能存在问题 - 两种语言返回了相同的数据")
                
    except Exception as e:
        print(f"❌ 结果比较失败: {e}")

def test_api_health():
    """测试API健康状态"""
    print("🏥 检查API健康状态...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API服务正常运行")
            return True
        else:
            print(f"❌ API健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到API服务: {e}")
        print("   请确保后端服务正在运行")
        return False

if __name__ == "__main__":
    print("🚀 语言切换功能测试")
    print("=" * 50)
    
    # 首先检查API健康状态
    if test_api_health():
        test_language_switching()
    else:
        print("\n❌ 测试终止：API服务不可用")
    
    print("\n" + "=" * 50)
    print("🏁 测试完成")
