#!/usr/bin/env python3
"""
纳甲六爻排盘系统启动脚本
"""

import uvicorn
from app import app

if __name__ == "__main__":
    print("🔮 纳甲六爻排盘系统启动中...")
    print("📖 API 文档地址: http://localhost:8000/docs")
    print("🌐 系统首页: http://localhost:8000")
    print("⏹️ 按 Ctrl+C 停止服务\n")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[".", "najia"],
        log_level="info"
    )
