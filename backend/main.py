"""
FastAPI主应用
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.api import roles, products, dialogue, dimensions, cases, models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    # 确保数据库目录存在
    import os
    db_path = settings.DATABASE_URL.split("///")[-1]
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)

    await init_db()
    try:
        print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} 启动成功！")
        print(f"📍 API地址: http://{settings.HOST}:{settings.PORT}/docs")
    except UnicodeEncodeError:
        print(f"{settings.APP_NAME} v{settings.APP_VERSION} 启动成功!")
        print(f"API地址: http://{settings.HOST}:{settings.PORT}/docs")

    yield  # 应用运行期间

    # 关闭时执行（如果需要）
    print("👋 应用关闭中...")


# 创建应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="保险销售智能陪练系统API",
    lifespan=lifespan  # 使用新的lifespan API
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册路由
app.include_router(roles.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(dialogue.router, prefix="/api")
app.include_router(dimensions.router, prefix="/api")
app.include_router(cases.router, prefix="/api")
app.include_router(models.router, prefix="/api", tags=["models"])


# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


# 健康检查
@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD  # 使用配置中的自动重载设置
    )
