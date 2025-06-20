# Najia 六爻排盘 API 文档

## 概述

Najia 是一个基于 FastAPI 的六爻排盘 Web 服务，提供传统六爻占卜的现代化 API 接口。

## 基础信息

- **服务地址**: `http://localhost:8000`
- **API 前缀**: `/api`
- **文档地址**: `http://localhost:8000/docs` (Swagger UI)
- **替代文档**: `http://localhost:8000/redoc` (ReDoc)

## API 端点列表

### 1. 健康检查

**GET** `/api/health`

检查服务状态。

**响应示例**:
```json
{
  "status": "healthy",
  "timestamp": "2025-06-20T16:02:00+08:00",
  "version": "1.0.0"
}
```

---

### 2. 手动起卦

**POST** `/api/gua`

根据手动输入的参数进行六爻排盘。

**请求体**:
```json
{
  "params": [4, 1, 3, 3, 4, 3],
  "gender": "男",
  "title": "测试起卦"
}
```

**参数说明**:
- `params`: 六个数字数组，每个数字代表一爻的初始状态
- `gender`: 性别（可选），支持 "男"、"女" 或空字符串
- `title`: 起卦标题（可选）

**响应示例**:
```json
{
  "success": true,
  "data": {
    "params": [4, 1, 3, 3, 4, 3],
    "gender": "男",
    "title": "测试起卦",
    "name": "火风鼎",
    "mark": "011101",
    "gong": "离",
    "solar": "2025-06-20T16:02:00+08:00",
    "lunar": {
      "xkong": "子丑",
      "gz": {
        "year": "乙巳",
        "month": "壬午", 
        "day": "庚申",
        "hour": "甲申"
      }
    },
    "god6": ["白虎", "玄武", "青龙", "朱雀", "勾陈", "螣蛇"],
    "dong": [0, 2, 3, 4, 5],
    "shiy": ["  ", "世", "  ", "  ", "应", "  "],
    "qin6": ["子孙", "官鬼", "妻财", "妻财", "子孙", "兄弟"],
    "qinx": ["辛丑土", "辛亥水", "辛酉金", "己酉金", "己未土", "己巳火"],
    "bian": {
      "name": "水泽节",
      "mark": ["▅▅▅▅▅▅", "▅▅▅▅▅▅", "▅▅  ▅▅", "▅▅  ▅▅", "▅▅▅▅▅▅", "▅▅  ▅▅"],
      "qin6": ["兄弟丁巳火", "父母丁卯木", "子孙丁丑土", "妻财戊申金", "子孙戊戌土", "官鬼戊子水"],
      "qinx": ["丁巳火", "丁卯木", "丁丑土", "戊申金", "戊戌土", "戊子水"],
      "gong": "坎",
      "type": "六合"
    },
    "main": {
      "mark": ["▅▅  ▅▅", "▅▅▅▅▅▅", "▅▅▅▅▅▅", "▅▅▅▅▅▅", "▅▅  ▅▅", "▅▅▅▅▅▅"],
      "type": "",
      "gong": "离",
      "name": "火风鼎"
    }
  },
  "rendered": "测：测试起卦\n\n公历：2025年 6月 20日 16时 2分\n...",
  "message": "手动起卦成功"
}
```

---

### 3. 随机起卦

**POST** `/api/random`

使用随机数生成六爻排盘。

**请求体**:
```json
{
  "gender": "女",
  "title": "随机测试"
}
```

**参数说明**:
- `gender`: 性别（可选）
- `title`: 起卦标题（可选）

**响应格式**: 与手动起卦相同

---

### 4. 时间起卦

**POST** `/api/time-gua`

根据当前时间进行六爻排盘。

**请求体**:
```json
{
  "gender": "",
  "title": "时间起卦"
}
```

**参数说明**:
- `gender`: 性别（可选）
- `title`: 起卦标题（可选）

**响应格式**: 与手动起卦相同

---

### 5. 获取常量

**GET** `/api/constants`

获取六爻系统中使用的各种常量。

**响应示例**:
```json
{
  "success": true,
  "data": {
    "tiangan": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
    "dizhi": ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"],
    "wuxing": ["金", "木", "水", "火", "土"],
    "bagua": ["乾", "坤", "震", "巽", "坎", "离", "艮", "兑"],
    "liushen": ["青龙", "朱雀", "勾陈", "螣蛇", "白虎", "玄武"],
    "liuqin": ["父母", "兄弟", "子孙", "妻财", "官鬼"]
  },
  "message": "获取常量成功"
}
```

---

### 6. 卦象分析

**GET** `/api/gua-analysis/{gua_name}`

根据卦名获取卦象的详细分析信息。

**路径参数**:
- `gua_name`: 卦名，如 "火风鼎"

**响应示例**:
```json
{
  "success": true,
  "data": {
    "name": "火风鼎",
    "gong": "离",
    "wuxing": "火",
    "description": "鼎卦代表变革、创新...",
    "interpretation": "此卦象征...",
    "structure": {
      "upper": "离",
      "lower": "巽"
    }
  },
  "message": "获取卦象分析成功"
}
```

---

## 数据字段说明

### 主要字段解释

- **params**: 起卦参数，6个数字组成的数组
- **name**: 卦名，如"火风鼎"
- **mark**: 卦象标记，如"011101"（0表示阴爻，1表示阳爻）
- **gong**: 所属宫位，如"离"
- **solar**: 公历时间
- **lunar**: 农历信息
  - **xkong**: 旬空
  - **gz**: 干支信息（年月日时）
- **god6**: 六神配置
- **dong**: 动爻位置数组
- **shiy**: 世应位置
- **qin6**: 六亲关系
- **qinx**: 纳甲配置
- **bian**: 变卦信息
- **main**: 主卦信息
- **rendered**: 格式化的排盘结果文本

### 响应状态

所有API都返回统一格式：
```json
{
  "success": boolean,
  "data": object,
  "rendered": string,
  "message": string
}
```

- **success**: 请求是否成功
- **data**: 具体数据内容
- **rendered**: 格式化的文本输出
- **message**: 操作结果描述

---

## 错误处理

### 常见错误码

- **400 Bad Request**: 请求参数错误
- **404 Not Found**: 资源不存在
- **422 Unprocessable Entity**: 数据验证失败
- **500 Internal Server Error**: 服务器内部错误

### 错误响应格式

```json
{
  "success": false,
  "detail": "错误详细信息",
  "message": "操作失败"
}
```

---

## 使用示例

### cURL 示例

1. **健康检查**:
```bash
curl -X GET "http://localhost:8000/api/health"
```

2. **手动起卦**:
```bash
curl -X POST "http://localhost:8000/api/gua" \
  -H "Content-Type: application/json" \
  -d '{"params": [4,1,3,3,4,3], "gender": "男", "title": "测试"}'
```

3. **随机起卦**:
```bash
curl -X POST "http://localhost:8000/api/random" \
  -H "Content-Type: application/json" \
  -d '{"gender": "女", "title": "随机测试"}'
```

4. **时间起卦**:
```bash
curl -X POST "http://localhost:8000/api/time-gua" \
  -H "Content-Type: application/json" \
  -d '{"title": "时间起卦"}'
```

5. **获取常量**:
```bash
curl -X GET "http://localhost:8000/api/constants"
```

6. **卦象分析**:
```bash
curl -X GET "http://localhost:8000/api/gua-analysis/火风鼎"
```

### Python 示例

```python
import requests

# 基础URL
BASE_URL = "http://localhost:8000/api"

# 手动起卦
response = requests.post(f"{BASE_URL}/gua", json={
    "params": [4, 1, 3, 3, 4, 3],
    "gender": "男",
    "title": "测试起卦"
})
result = response.json()
print(result["rendered"])

# 随机起卦
response = requests.post(f"{BASE_URL}/random", json={
    "gender": "女",
    "title": "随机起卦"
})
result = response.json()
print(result["data"]["name"])

# 获取常量
response = requests.get(f"{BASE_URL}/constants")
constants = response.json()["data"]
print(constants["bagua"])
```

### JavaScript 示例

```javascript
// 使用 fetch API
async function callAPI() {
    // 手动起卦
    const response = await fetch('http://localhost:8000/api/gua', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            params: [4, 1, 3, 3, 4, 3],
            gender: '男',
            title: '测试起卦'
        })
    });
    
    const result = await response.json();
    console.log(result.rendered);
}
```

---

## 启动服务

### 开发环境

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务（方式1）
python start_server.py

# 启动服务（方式2）
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Docker 部署

```bash
# 构建镜像
docker build -t najia-api .

# 运行容器
docker run -d -p 8000:8000 najia-api
```

---

## 注意事项

1. **参数范围**: 手动起卦的 params 数组中每个数字建议在 1-6 之间
2. **编码**: 所有文本数据使用 UTF-8 编码
3. **时区**: 时间默认使用系统时区，建议使用 UTC+8（北京时间）
4. **性能**: 单次排盘计算通常在 100ms 内完成
5. **并发**: 支持多并发请求，无状态设计

---

## 更新日志

### v1.0.0 (2025-06-20)
- 初始版本发布
- 实现基础六爻排盘功能
- 支持手动、随机、时间起卦
- 提供 Web 界面和 API 接口
- 完整的 API 文档和测试用例

---

## 联系信息

如有问题或建议，请提交 Issue 或联系开发团队。

项目基于开源 najia 库：https://github.com/bopo/najia
