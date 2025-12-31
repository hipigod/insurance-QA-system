"""
应用配置管理
"""
import os
from pathlib import Path
from typing import ClassVar
from pydantic_settings import BaseSettings
from typing import Optional


# 获取backend目录的绝对路径
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基础配置
    APP_NAME: str = "保险销售智能陪练系统"
    APP_VERSION: str = "1.2.0"
    DEBUG: bool = True

    # 服务器配置
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True  # 自动重载(开发模式)

    # 数据库配置 - 使用绝对路径
    DATABASE_URL: str = f"sqlite+aiosqlite:///{BASE_DIR}/data/insurance_practice.db"

    # AI模型配置
    DEFAULT_MODEL: str = "qwen-plus"  # 默认使用通义千问
    MODEL_API_KEY: Optional[str] = None
    MODEL_API_BASE: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # 对话配置
    MAX_DIALOGUE_ROUNDS: int = 20
    AI_RESPONSE_TIMEOUT: int = 10  # 秒
    AI_TEMPERATURE: float = 0.7

    # CORS配置
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:8080"]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
