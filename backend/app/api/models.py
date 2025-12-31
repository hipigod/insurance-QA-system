"""
模型配置管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from app.core.database import get_db
from app.models.models import ModelConfig
from app.models.schemas import ModelConfigResponse, ModelConfigCreate, ModelConfigUpdate

router = APIRouter(prefix="/models", tags=["模型配置"])


@router.get("/", response_model=List[ModelConfigResponse])
async def get_models(db: AsyncSession = Depends(get_db)):
    """获取所有模型配置"""
    result = await db.execute(select(ModelConfig))
    models = result.scalars().all()
    return models


@router.get("/{model_id}", response_model=ModelConfigResponse)
async def get_model(model_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个模型配置"""
    result = await db.execute(select(ModelConfig).where(ModelConfig.id == model_id))
    model = result.scalar_one_or_none()

    if not model:
        raise HTTPException(status_code=404, detail="Model config not found")

    return model


@router.post("/", response_model=ModelConfigResponse)
async def create_model(model: ModelConfigCreate, db: AsyncSession = Depends(get_db)):
    """创建模型配置"""
    # 检查模型名称是否已存在
    result = await db.execute(select(ModelConfig).where(ModelConfig.model_name == model.model_name))
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Model name already exists")

    # 如果设置为激活，先取消其他模型的激活状态
    if model.is_active:
        await db.execute(update(ModelConfig).values(is_active=0))

    # 创建新模型配置
    db_model = ModelConfig(**model.dict())
    db.add(db_model)
    await db.commit()
    await db.refresh(db_model)

    return db_model


@router.put("/{model_id}", response_model=ModelConfigResponse)
async def update_model(model_id: int, model: ModelConfigUpdate, db: AsyncSession = Depends(get_db)):
    """更新模型配置"""
    result = await db.execute(select(ModelConfig).where(ModelConfig.id == model_id))
    db_model = result.scalar_one_or_none()

    if not db_model:
        raise HTTPException(status_code=404, detail="Model config not found")

    # 如果设置为激活，先取消其他模型的激活状态
    if model.is_active:
        await db.execute(update(ModelConfig).values(is_active=0).where(ModelConfig.id != model_id))

    # 更新模型配置
    for key, value in model.dict(exclude_unset=True).items():
        setattr(db_model, key, value)

    await db.commit()
    await db.refresh(db_model)

    return db_model


@router.delete("/{model_id}")
async def delete_model(model_id: int, db: AsyncSession = Depends(get_db)):
    """删除模型配置"""
    result = await db.execute(select(ModelConfig).where(ModelConfig.id == model_id))
    db_model = result.scalar_one_or_none()

    if not db_model:
        raise HTTPException(status_code=404, detail="Model config not found")

    await db.delete(db_model)
    await db.commit()

    return {"message": "Model config deleted successfully"}


@router.post("/{model_id}/activate")
async def activate_model(model_id: int, db: AsyncSession = Depends(get_db)):
    """激活指定模型"""
    result = await db.execute(select(ModelConfig).where(ModelConfig.id == model_id))
    db_model = result.scalar_one_or_none()

    if not db_model:
        raise HTTPException(status_code=404, detail="Model config not found")

    # 取消所有模型的激活状态
    await db.execute(update(ModelConfig).values(is_active=0))

    # 激活指定模型
    db_model.is_active = True
    await db.commit()

    return {"message": f"Model {db_model.model_name} activated successfully"}
