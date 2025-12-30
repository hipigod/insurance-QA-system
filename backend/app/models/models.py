"""
数据库模型定义
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base


class CustomerRole(Base):
    """客户角色表"""
    __tablename__ = "customer_roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="角色名称")
    description = Column(Text, comment="角色简介")
    difficulty = Column(String(20), comment="难度等级")
    system_prompt = Column(Text, nullable=False, comment="角色提示词")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class InsuranceProduct(Base):
    """保险产品表"""
    __tablename__ = "insurance_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="产品名称")
    description = Column(Text, comment="产品简介")
    product_type = Column(String(50), comment="产品类型")
    coverage = Column(Text, comment="保障范围")
    premium_range = Column(String(100), comment="保费范围")
    target_audience = Column(String(200), comment="适用人群")
    detailed_info = Column(Text, comment="产品详细信息")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ScoringDimension(Base):
    """评分维度表"""
    __tablename__ = "scoring_dimensions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, comment="维度名称")
    description = Column(Text, comment="维度描述")
    weight = Column(Float, default=25.0, comment="权重(0-100)")
    evaluation_prompt = Column(Text, comment="评分依据提示词")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PracticeRecord(Base):
    """练习记录表"""
    __tablename__ = "practice_records"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, nullable=False, comment="角色ID")
    product_id = Column(Integer, nullable=False, comment="产品ID")
    dialogue_data = Column(JSON, comment="完整对话数据")
    score_data = Column(JSON, comment="评分数据")
    total_score = Column(Float, comment="总分")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ModelConfig(Base):
    """AI模型配置表"""
    __tablename__ = "model_configs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False, unique=True, comment="模型名称")
    provider = Column(String(100), comment="提供商")
    api_key = Column(String(500), comment="API Key(加密存储)")
    api_base = Column(String(500), comment="API Base URL")
    is_active = Column(Integer, default=1, comment="是否启用")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ExcellentCase(Base):
    """优秀案例库表"""
    __tablename__ = "excellent_cases"

    id = Column(Integer, primary_key=True, index=True)
    weakness_type = Column(String(100), nullable=False, comment="薄弱环节类型")
    case_content = Column(Text, nullable=False, comment="案例内容")
    dialogue_node = Column(String(50), comment="对应对话节点")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
