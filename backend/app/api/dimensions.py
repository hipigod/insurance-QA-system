"""
评分维度管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import ScoringDimension
from app.models.schemas import ScoringDimensionCreate, ScoringDimensionUpdate, ScoringDimensionResponse, ResponseModel

router = APIRouter(prefix="/dimensions", tags=["评分维度"])


@router.get("/", response_model=List[ScoringDimensionResponse])
async def get_dimensions(db: AsyncSession = Depends(get_db)):
    """获取所有评分维度"""
    result = await db.execute(select(ScoringDimension))
    dimensions = result.scalars().all()
    return dimensions


@router.post("/", response_model=ScoringDimensionResponse)
async def create_dimension(dimension_data: ScoringDimensionCreate, db: AsyncSession = Depends(get_db)):
    """创建新评分维度"""
    new_dimension = ScoringDimension(**dimension_data.model_dump())

    db.add(new_dimension)
    await db.commit()
    await db.refresh(new_dimension)

    return new_dimension


@router.put("/{dimension_id}", response_model=ScoringDimensionResponse)
async def update_dimension(
    dimension_id: int,
    dimension_data: ScoringDimensionUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新评分维度"""
    result = await db.execute(select(ScoringDimension).where(ScoringDimension.id == dimension_id))
    dimension = result.scalar_one_or_none()

    if not dimension:
        raise HTTPException(status_code=404, detail="评分维度不存在")

    # 更新字段
    update_data = dimension_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dimension, field, value)

    await db.commit()
    await db.refresh(dimension)

    return dimension


@router.delete("/{dimension_id}")
async def delete_dimension(dimension_id: int, db: AsyncSession = Depends(get_db)):
    """删除评分维度"""
    result = await db.execute(select(ScoringDimension).where(ScoringDimension.id == dimension_id))
    dimension = result.scalar_one_or_none()

    if not dimension:
        raise HTTPException(status_code=404, detail="评分维度不存在")

    await db.delete(dimension)
    await db.commit()

    return ResponseModel(message="删除成功")
