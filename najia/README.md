纳甲六爻排盘项目 (FastAPI 版本)
================

[![image](https://img.shields.io/pypi/v/najia.svg)](https://pypi.python.org/pypi/najia)
[![image](https://img.shields.io/travis/bopo/najia.svg)](https://travis-ci.org/bopo/najia)
[![Documentation Status](https://readthedocs.org/projects/najia/badge/?version=latest)](https://najia.readthedocs.io/en/latest/?badge=latest)
[![Updates](https://pyup.io/repos/github/bopo/najia/shield.svg)](https://pyup.io/repos/github/bopo/najia/)

基于 FastAPI 的纳甲六爻排盘系统，提供 Web API 和用户界面。

-   免费开源: MIT license
-   在线文档: <https://najia.readthedocs.io>
-   API 文档: 启动后访问 `/docs`

## 快速开始

### 安装依赖
```bash
pip install fastapi uvicorn pydantic arrow jinja2 lunar-python
```

### 启动服务
```bash
# 方式1：直接运行
python main.py

# 方式2：使用 uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --reload

# 方式3：使用 poetry (推荐)
poetry install
poetry run python main.py
```

### 访问服务
- 主页: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 交互式文档: http://localhost:8000/redoc

## API 端点

### 1. 起卦排盘
```http
POST /api/gua
Content-Type: application/json

{
    "params": [2, 2, 1, 2, 4, 2],
    "title": "求财运",
    "gender": "男",
    "date": "2024-01-01 12:00:00",
    "guaci": true,
    "verbose": 1
}
```

### 2. 随机起卦
```http
GET /api/random
```

### 3. 根据卦码查询
```http
GET /api/gua/010010
```

### 4. 健康检查
```http
GET /api/health
```

Features
--------

-   全部安易卦爻
-   函数独立编写
-   测试各个函数
-   重新命名函数

阳历，阴历（干支，旬空）

-   卦符: mark (001000)，自下而上
-   卦名: name
-   变爻: bian
-   卦宫: gong
-   六亲: qin6
-   六神: god6
-   世爻: shiy, ying
-   纳甲: naja
-   纳甲五行: dzwx
-   卦宫五行: gowx

修复问题
--------

-   解决: 六神不对
-   解决: 世应也有点小BUG , 地天泰卦的世爻为3, 应爻为6
-   解决: 归魂卦世爻为3 此处返回4, 需要修改

\* 解决: 归魂卦的六亲是不对的,原因是utils.py里
判断六爻卦的卦宫名时,优先判读了if index in (1, 2, 3, 6)
而归魂卦的世爻也在3爻,被这个条件带走了. 解决: elif hun==\'归魂\'
这个条件调到前面即可 \* 解决: 还有一个不知是否算是错误的地方,就是bian
变卦中的六亲,
程序中是按变卦所在的本宫卦来定的,而不是按初始卦所属的本宫卦来定的六亲.

Credits
-------

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
