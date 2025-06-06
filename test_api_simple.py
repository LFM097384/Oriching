import requests
import json

# 测试手动占卜API
def test_manual_divination():
    url = "http://localhost:8000/api/divination/manual"
    
    # 测试数据：[7,7,7,6,7,7] 应该是风天小畜 #9，第4爻变
    test_data = {
        "lines": [7, 7, 7, 6, 7, 7]
    }
    
    try:
        print(f"正在测试手动占卜API：{url}")
        print(f"测试数据：{test_data}")
        
        response = requests.post(url, json=test_data)
        
        print(f"状态码：{response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("成功响应：")
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"错误响应：{response.text}")
            
    except requests.exceptions.ConnectionError:
        print("错误：无法连接到服务器。请确保后端服务正在运行。")
    except Exception as e:
        print(f"错误：{e}")

if __name__ == "__main__":
    test_manual_divination()
