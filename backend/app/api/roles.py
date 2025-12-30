"""
客户角色管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import CustomerRole
from app.models.schemas import RoleCreate, RoleUpdate, RoleResponse, ResponseModel

router = APIRouter(prefix="/roles", tags=["客户角色"])


@router.get("/", response_model=List[RoleResponse])
async def get_roles(db: AsyncSession = Depends(get_db)):
    """获取所有角色列表"""
    result = await db.execute(select(CustomerRole))
    roles = result.scalars().all()
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    """获取单个角色详情"""
    result = await db.execute(select(CustomerRole).where(CustomerRole.id == role_id))
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    return role


@router.post("/", response_model=RoleResponse)
async def create_role(role_data: RoleCreate, db: AsyncSession = Depends(get_db)):
    """创建新角色"""
    new_role = CustomerRole(**role_data.model_dump())

    db.add(new_role)
    await db.commit()
    await db.refresh(new_role)

    return new_role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db)
):
    """更新角色信息"""
    result = await db.execute(select(CustomerRole).where(CustomerRole.id == role_id))
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 更新字段
    update_data = role_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(role, field, value)

    await db.commit()
    await db.refresh(role)

    return role


@router.delete("/{role_id}")
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    """删除角色"""
    result = await db.execute(select(CustomerRole).where(CustomerRole.id == role_id))
    role = result.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    await db.delete(role)
    await db.commit()

    return ResponseModel(message="删除成功")
