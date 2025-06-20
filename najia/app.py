"""
FastAPI 纳甲六爻排盘系统 - 修复版本
"""
from datetime import datetime
from typing import List, Optional
import json

import arrow
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field, field_validator

from najia.najia import Najia

app = FastAPI(
    title="纳甲六爻排盘系统",
    description="基于传统六爻预测学的在线排盘系统，提供完整的六爻起卦、分析和排盘功能",
    version="2.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def clean_data_for_json(data):
    """清理数据中的不可序列化对象"""
    if isinstance(data, dict):
        cleaned = {}
        for key, value in data.items():
            if hasattr(value, 'isoformat'):  # Arrow or datetime objects
                cleaned[key] = value.isoformat()
            elif isinstance(value, (dict, list)):
                cleaned[key] = clean_data_for_json(value)
            else:
                cleaned[key] = value
        return cleaned
    elif isinstance(data, list):
        return [clean_data_for_json(item) for item in data]
    elif hasattr(data, 'isoformat'):  # Arrow or datetime objects
        return data.isoformat()
    else:
        return data


class GuaRequest(BaseModel):
    params: List[int] = Field(..., description="六个数字，代表六爻参数")
    gender: Optional[str] = Field(default="", description="性别")
    title: Optional[str] = Field(default="", description="起卦标题")
    date: Optional[str] = Field(default=None, description="指定时间")
    guaci: Optional[bool] = Field(default=False, description="是否显示卦辞")
    verbose: Optional[int] = Field(default=1, description="显示详细程度")

    @field_validator('params')
    @classmethod
    def validate_params(cls, v):
        if len(v) != 6:
            raise ValueError('必须提供6个参数')
        if not all(1 <= x <= 4 for x in v):
            raise ValueError('参数必须在1-4之间')
        return v

class RandomGuaRequest(BaseModel):
    gender: Optional[str] = Field(default="", description="性别")
    title: Optional[str] = Field(default="随机起卦", description="标题")

class TimeGuaRequest(BaseModel):
    gender: Optional[str] = Field(default="", description="性别")
    title: Optional[str] = Field(default="时间起卦", description="标题")


@app.get("/", response_class=HTMLResponse)
async def index():
    """首页"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>纳甲六爻排盘系统</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Microsoft YaHei', '微软雅黑', Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            .container { 
                max-width: 900px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                border-radius: 15px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            h1 { 
                color: #2c3e50; 
                text-align: center; 
                margin-bottom: 40px; 
                font-size: 2.5em;
            }
            .form-group { margin-bottom: 25px; }
            label { 
                display: block; 
                margin-bottom: 8px; 
                font-weight: 600; 
                color: #34495e;
            }
            input, select { 
                width: 100%; 
                padding: 12px 15px; 
                border: 2px solid #e0e6ed;
                border-radius: 8px; 
                font-size: 14px;
                transition: all 0.3s ease;
            }
            input:focus, select:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            button { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white; 
                padding: 15px 40px; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px;
                font-weight: 600;
                width: 100%;
                margin-top: 20px;
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            }
            .result { 
                margin-top: 30px; 
                padding: 25px; 
                background: #f8f9fa; 
                border-radius: 10px; 
                white-space: pre-wrap; 
                font-family: 'Courier New', monospace;
                max-height: 500px;
                overflow-y: auto;
                display: none;
            }
            .example { 
                background: #e3f2fd;
                padding: 20px; 
                border-radius: 10px; 
                margin-bottom: 30px;
            }
            .quick-buttons {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 10px;
                margin-top: 10px;
            }
            .quick-btn {
                padding: 8px 12px;
                background: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                cursor: pointer;
                text-align: center;
                font-size: 13px;
            }
            .quick-btn:hover {
                background: #667eea;
                color: white;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔮 纳甲六爻排盘系统</h1>
            
            <div class="example">
                <h3>📖 使用说明</h3>
                <ul>
                    <li><strong>1 = 老阳 (━━━━━━)</strong> - 阳爻不变</li>
                    <li><strong>2 = 少阴 (━━  ━━)</strong> - 阴爻不变</li>
                    <li><strong>3 = 老阴 (━━  ━━)</strong> - 阴爻动变</li>
                    <li><strong>4 = 少阳 (━━━━━━)</strong> - 阳爻动变</li>
                </ul>
            </div>
            
            <form id="guaForm">
                <div class="form-group">
                    <label for="params">六爻参数 (6个数字，用逗号分隔):</label>
                    <input type="text" id="params" placeholder="例如：2,2,1,2,4,2" value="2,2,1,2,4,2">
                    <div class="quick-buttons">
                        <div class="quick-btn" onclick="setParams('1,1,1,1,1,1')">乾卦</div>
                        <div class="quick-btn" onclick="setParams('2,2,2,2,2,2')">坤卦</div>
                        <div class="quick-btn" onclick="setParams('1,2,1,2,1,2')">泰卦</div>
                        <div class="quick-btn" onclick="randomParams()">随机</div>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="title">求卦事项:</label>
                    <input type="text" id="title" placeholder="请输入您要问卜的事情">
                </div>
                
                <div class="form-group">
                    <label for="gender">性别:</label>
                    <select id="gender">
                        <option value="">请选择</option>
                        <option value="男">男</option>
                        <option value="女">女</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="date">起卦时间:</label>
                    <input type="datetime-local" id="date">
                </div>
                
                <div class="form-group">
                    <label>
                        <input type="checkbox" id="guaci" style="width: auto; margin-right: 10px;">
                        显示卦辞解释
                    </label>
                </div>
                
                <button type="submit">🔮 开始排盘</button>
            </form>
            
            <div id="result" class="result"></div>
        </div>

        <script>
            function setParams(params) {
                document.getElementById('params').value = params;
            }
            
            function randomParams() {
                const random = Array.from({length: 6}, () => Math.floor(Math.random() * 4) + 1);
                document.getElementById('params').value = random.join(',');
            }
            
            document.getElementById('guaForm').onsubmit = async function(e) {
                e.preventDefault();
                
                const params = document.getElementById('params').value.split(',').map(x => parseInt(x.trim()));
                const title = document.getElementById('title').value;
                const gender = document.getElementById('gender').value;
                const date = document.getElementById('date').value;
                const guaci = document.getElementById('guaci').checked;
                
                if (params.length !== 6 || params.some(x => isNaN(x) || x < 1 || x > 4)) {
                    alert('请输入6个1-4之间的数字');
                    return;
                }
                
                const data = { params, title, gender, guaci, verbose: 1 };
                if (date) data.date = date.replace('T', ' ') + ':00';
                
                try {
                    const response = await fetch('/api/gua', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    const resultDiv = document.getElementById('result');
                    resultDiv.style.display = 'block';
                    resultDiv.textContent = result.rendered || JSON.stringify(result, null, 2);
                    resultDiv.scrollIntoView({ behavior: 'smooth' });
                } catch (error) {
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').textContent = '请求失败：' + error.message;
                }
            };
            
            // 设置默认时间
            document.getElementById('date').value = new Date().toISOString().slice(0, 16);
        </script>
    </body>
    </html>
    """


@app.post("/api/gua")
async def create_gua(request: GuaRequest):
    """起卦排盘API"""
    try:
        najia = Najia(verbose=request.verbose)
        gua = najia.compile(
            params=request.params,
            gender=request.gender,
            date=request.date,
            title=request.title,
            guaci=request.guaci
        )
        
        rendered = gua.render()
        
        # 确保返回数据中的爻图像使用0和1格式
        cleaned_data = clean_data_for_json(gua.data)
        
        # 添加简化的mark字段（0和1格式）
        if 'mark' in cleaned_data:
            cleaned_data['mark_binary'] = cleaned_data['mark']  # 原本就是01格式
        
        # 如果main字段存在mark，也改为01格式
        if 'main' in cleaned_data and 'mark' in cleaned_data['main']:
            cleaned_data['main']['mark_binary'] = cleaned_data['mark']
            
        # 如果bian字段存在mark，也改为01格式  
        if 'bian' in cleaned_data and cleaned_data['bian'] and 'mark' in cleaned_data['bian']:
            cleaned_data['bian']['mark_binary'] = cleaned_data['bian']['mark']
        
        return {
            "success": True,
            "data": cleaned_data,
            "rendered": rendered,
            "message": "起卦成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"起卦失败: {str(e)}")


@app.post("/api/random")
async def random_gua(request: Optional[RandomGuaRequest] = None):
    """随机起卦"""
    import random
    
    params = [random.randint(1, 4) for _ in range(6)]
    
    try:
        najia = Najia(verbose=1)
        gua = najia.compile(
            params=params, 
            title=request.title if request else "随机起卦",
            gender=request.gender if request else ""
        )
        rendered = gua.render()
        
        # 确保返回数据中的爻图像使用0和1格式
        cleaned_data = clean_data_for_json(gua.data)
        
        # 添加简化的mark字段（0和1格式）
        if 'mark' in cleaned_data:
            cleaned_data['mark_binary'] = cleaned_data['mark']
        
        # 如果main字段存在mark，也改为01格式
        if 'main' in cleaned_data and 'mark' in cleaned_data['main']:
            cleaned_data['main']['mark_binary'] = cleaned_data['mark']
            
        # 如果bian字段存在mark，也改为01格式  
        if 'bian' in cleaned_data and cleaned_data['bian'] and 'mark' in cleaned_data['bian']:
            cleaned_data['bian']['mark_binary'] = cleaned_data['bian']['mark']
        
        return {
            "success": True,
            "data": cleaned_data,
            "rendered": rendered,
            "message": "随机起卦成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"随机起卦失败: {str(e)}")


@app.post("/api/time-gua")
async def time_gua(request: Optional[TimeGuaRequest] = None):
    """基于当前时间起卦"""
    try:
        import hashlib
        
        now = arrow.now()
        time_str = now.format('YYYY-MM-DD-HH-mm-ss')
        hash_obj = hashlib.md5(time_str.encode())
        hash_hex = hash_obj.hexdigest()
        
        params = []
        for i in range(6):
            seed = int(hash_hex[i*2:i*2+2], 16)
            param = (seed % 4) + 1
            params.append(param)
        
        najia = Najia(verbose=1)
        gua = najia.compile(
            params=params, 
            title=request.title if request else "时间起卦",
            gender=request.gender if request else "",
            date=now.format('YYYY-MM-DD HH:mm')
        )
        rendered = gua.render()
        
        # 确保返回数据中的爻图像使用0和1格式
        cleaned_data = clean_data_for_json(gua.data)
        
        # 添加简化的mark字段（0和1格式）
        if 'mark' in cleaned_data:
            cleaned_data['mark_binary'] = cleaned_data['mark']
        
        # 如果main字段存在mark，也改为01格式
        if 'main' in cleaned_data and 'mark' in cleaned_data['main']:
            cleaned_data['main']['mark_binary'] = cleaned_data['mark']
            
        # 如果bian字段存在mark，也改为01格式  
        if 'bian' in cleaned_data and cleaned_data['bian'] and 'mark' in cleaned_data['bian']:
            cleaned_data['bian']['mark_binary'] = cleaned_data['bian']['mark']
        
        return {
            "success": True,
            "data": cleaned_data,
            "rendered": rendered,
            "message": "时间起卦成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"时间起卦失败: {str(e)}")


@app.get("/api/constants")
async def get_constants():
    """获取系统常量信息"""
    try:
        from najia.const import GUA64, GUAS, QING6, SHEN6, XING5
        
        return {
            "success": True,
            "data": {
                "gua64": GUA64,
                "guas": GUAS,
                "qing6": QING6,
                "shen6": SHEN6,
                "xing5": XING5,
            },
            "message": "获取常量信息成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取常量信息失败: {str(e)}")


@app.get("/api/gua-analysis/{gua_name}")
async def analyze_gua(gua_name: str):
    """分析特定卦象的基本信息"""
    try:
        from najia.const import GUA64
        
        gua_code = None
        for code, name in GUA64.items():
            if name == gua_name:
                gua_code = code
                break
        
        if not gua_code:
            raise HTTPException(status_code=404, detail=f"未找到卦象: {gua_name}")
        
        params = [2 if c == '0' else 1 for c in gua_code]
        
        najia = Najia(verbose=1)
        gua = najia.compile(params=params, title=f"分析{gua_name}")
        rendered = gua.render()
        
        return {
            "success": True,
            "gua_name": gua_name,
            "gua_code": gua_code,
            "params": params,
            "data": clean_data_for_json(gua.data),
            "rendered": rendered,
            "message": f"分析{gua_name}成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析卦象失败: {str(e)}")


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "纳甲六爻排盘系统运行正常"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
