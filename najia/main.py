#!/usr/bin/env python3
"""
FastAPI 纳甲六爻排盘系统启动脚本
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["najia"],
        log_level="info"
    )
