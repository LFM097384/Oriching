"""
FastAPI 纳甲六爻排盘系统测试
"""
import json
import requests
from datetime import datetime

# API 基础URL
BASE_URL = "http://localhost:8000"


def test_health_check():
    """测试健康检查"""
    response = requests.get(f"{BASE_URL}/api/health")
    print("健康检查:", response.json())
    return response.status_code == 200


def test_random_gua():
    """测试随机起卦"""
    response = requests.post(f"{BASE_URL}/api/random", json={})
    result = response.json()
    print("随机起卦成功:", result["success"])
    if result["success"]:
        print("卦象参数:", result["data"]["params"])
        print("卦象标记:", result["data"]["mark"])
        print("卦象标记(二进制):", result["data"].get("mark_binary", "未找到"))
        print("卦象内容预览:", result["rendered"][:100] + "...")
    return response.status_code == 200


def test_create_gua():
    """测试指定参数起卦"""
    data = {
        "params": [2, 2, 1, 2, 4, 2],
        "title": "测试起卦",
        "gender": "男",
        "date": "2024-01-01 12:00:00",
        "guaci": True,
        "verbose": 1
    }
    
    response = requests.post(
        f"{BASE_URL}/api/gua",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    result = response.json()
    print("指定参数起卦成功:", result["success"])
    if result["success"]:
        print("卦象参数:", result["data"]["params"])
        print("卦象标记:", result["data"]["mark"])
        print("卦象标记(二进制):", result["data"].get("mark_binary", "未找到"))
        print("卦象内容预览:", result["rendered"][:100] + "...")
    return response.status_code == 200


def test_time_gua():
    """测试时间起卦"""
    response = requests.post(f"{BASE_URL}/api/time-gua", json={})
    result = response.json()
    print("时间起卦成功:", result["success"])
    if result["success"]:
        print("卦象参数:", result["data"]["params"])
        print("卦象标记:", result["data"]["mark"])
        print("卦象标记(二进制):", result["data"].get("mark_binary", "未找到"))
        print("卦象内容预览:", result["rendered"][:100] + "...")
    return response.status_code == 200


def test_get_constants():
    """测试获取系统常量"""
    response = requests.get(f"{BASE_URL}/api/constants")
    result = response.json()
    print("获取常量成功:", result["success"])
    if result["success"]:
        print("可用常量:", list(result["data"].keys()))
    return response.status_code == 200


def test_analyze_gua():
    """测试卦象分析"""
    gua_name = "乾为天"
    response = requests.get(f"{BASE_URL}/api/gua-analysis/{gua_name}")
    result = response.json()
    print(f"分析{gua_name}成功:", result["success"])
    if result["success"]:
        print("卦码:", result["gua_code"])
        print("参数:", result["params"])
    return response.status_code == 200


def run_all_tests():
    """运行所有测试"""
    print("开始测试 FastAPI 纳甲六爻排盘系统...")
    print("=" * 50)
    
    tests = [
        ("健康检查", test_health_check),
        ("随机起卦", test_random_gua),
        ("指定参数起卦", test_create_gua),
        ("时间起卦", test_time_gua),
        ("获取常量", test_get_constants),
        ("卦象分析", test_analyze_gua),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n测试: {test_name}")
        print("-" * 30)
        try:
            success = test_func()
            results.append((test_name, success))
            print(f"结果: {'✓ 通过' if success else '✗ 失败'}")
        except Exception as e:
            print(f"结果: ✗ 错误 - {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("测试汇总:")
    for test_name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    print(f"\n总计: {passed_tests}/{total_tests} 测试通过")


if __name__ == "__main__":
    run_all_tests()
