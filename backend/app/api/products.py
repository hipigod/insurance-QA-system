"""
保险产品管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import InsuranceProduct
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, ResponseModel

router = APIRouter(prefix="/products", tags=["保险产品"])


@router.get("/", response_model=List[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    """获取所有产品列表"""
    result = await db.execute(select(InsuranceProduct))
    products = result.scalars().all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个产品详情"""
    result = await db.execute(select(InsuranceProduct).where(InsuranceProduct.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    return product


@router.post("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: AsyncSession = Depends(get_db)):
    """创建新产品"""
    new_product = InsuranceProduct(**product_data.model_dump())

    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)

    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新产品信息"""
    result = await db.execute(select(InsuranceProduct).where(InsuranceProduct.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    # 更新字段
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    return product


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """删除产品"""
    result = await db.execute(select(InsuranceProduct).where(InsuranceProduct.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    await db.delete(product)
    await db.commit()

    return ResponseModel(message="删除成功")
