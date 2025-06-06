"""
Main application file for the I Ching Divination API.

This FastAPI application provides endpoints for:
- Performing divination readings
- Querying hexagram information
- Managing hexagram data

The application is structured with:
- Models: Pydantic schemas for data validation
- Routers: API endpoint definitions
- Utils: Business logic and data management
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from routers import divination_router, hexagrams_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the application.
    """
    # Startup
    print("🚀 易经占卜 API 启动中...")
    print("📚 加载卦象数据...")
    
    yield
    
    # Shutdown  
    print("🛑 易经占卜 API 关闭中...")


# Initialize FastAPI application
app = FastAPI(
    title="易经占卜 API",
    description="""
    基于传统易经理论的智能占卜API系统
    
    ## 功能特色
    
    * **智能占卜**: 使用传统投币方法生成卦象
    * **完整解释**: 提供详细的卦象解读和人生指导
    * **卦象查询**: 支持多种方式查询64卦信息
    * **变卦分析**: 自动处理变爻和变卦分析
    
    ## 使用说明
    
    1. 准备一个明确的问题
    2. 调用占卜接口获得卦象
    3. 根据解释做出理性判断
    4. 重要决策请咨询专业人士
    
    **注意**: 本系统仅供娱乐和参考，不能替代专业建议。
    """,
    version="2.0.0",
    contact={
        "name": "易经AI团队",
        "email": "contact@yijing-ai.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        # Add production domains here
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(divination_router)
app.include_router(hexagrams_router)


@app.get("/", tags=["root"])
async def root() -> dict[str, str | dict[str, str]]:
    """
    Root endpoint - API health check.
    
    Returns:
        dict: API status and basic information
    """
    return {
        "message": "易经占卜 API 服务运行中",
        "status": "healthy",
        "version": "2.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "divination": "/api/divination",
            "hexagrams": "/api/hexagrams",
            "help": "/api/divination/help"
        }
    }


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """
    Health check endpoint for monitoring.
    
    Returns:
        dict: Detailed health status
    """
    return {
        "status": "healthy",
        "service": "I Ching Divination API",
        "version": "2.0.0",
        "timestamp": "2025-06-02T09:00:00Z"
    }


if __name__ == "__main__":
    """
    Run the application directly with uvicorn.
    
    For production, use:
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    """
    # Type ignore for uvicorn.run type annotation issue
    uvicorn.run(  # type: ignore
        app="main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
