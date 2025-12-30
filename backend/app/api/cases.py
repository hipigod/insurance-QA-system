"""
优秀案例管理API
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import ExcellentCase
from app.models.schemas import ExcellentCaseCreate, ExcellentCaseResponse, ResponseModel

router = APIRouter(prefix="/cases", tags=["优秀案例"])


@router.get("/", response_model=List[ExcellentCaseResponse])
async def get_cases(db: AsyncSession = Depends(get_db)):
    """获取所有优秀案例"""
    result = await db.execute(select(ExcellentCase))
    cases = result.scalars().all()
    return cases


@router.post("/", response_model=ExcellentCaseResponse)
async def create_case(case_data: ExcellentCaseCreate, db: AsyncSession = Depends(get_db)):
    """创建新案例"""
    new_case = ExcellentCase(**case_data.model_dump())

    db.add(new_case)
    await db.commit()
    await db.refresh(new_case)

    return new_case


@router.put("/{case_id}", response_model=ExcellentCaseResponse)
async def update_case(
    case_id: int,
    case_data: ExcellentCaseCreate,
    db: AsyncSession = Depends(get_db)
):
    """更新案例"""
    result = await db.execute(select(ExcellentCase).where(ExcellentCase.id == case_id))
    case = result.scalar_one_or_none()

    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")

    # 更新字段
    update_data = case_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    await db.commit()
    await db.refresh(case)

    return case


@router.delete("/{case_id}")
async def delete_case(case_id: int, db: AsyncSession = Depends(get_db)):
    """删除案例"""
    result = await db.execute(select(ExcellentCase).where(ExcellentCase.id == case_id))
    case = result.scalar_one_or_none()

    if not case:
        raise HTTPException(status_code=404, detail="案例不存在")

    await db.delete(case)
    await db.commit()

    return ResponseModel(message="删除成功")
