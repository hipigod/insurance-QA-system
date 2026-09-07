"""
模型配置管理API - 配置持久化到 data/model_config.json
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.core import model_store
from app.models.schemas import (
    ModelConfigResponse,
    ModelConfigCreate,
    ModelConfigUpdate,
)

router = APIRouter(prefix="/models", tags=["模型配置"])


def _to_response(m: dict) -> ModelConfigResponse:
    """内部dict转响应模型（不回传api_key）"""
    return ModelConfigResponse(
        id=m["id"],
        model_name=m["model_name"],
        provider=m.get("provider") or None,
        api_base=m.get("api_base") or None,
        is_active=bool(m.get("is_active", True)),
        created_at=m.get("created_at", ""),
        updated_at=m.get("updated_at", ""),
    )


@router.get("/", response_model=List[ModelConfigResponse])
async def get_models():
    """获取所有模型配置"""
    return [_to_response(m) for m in model_store.load_models()]


@router.get("/{model_id}", response_model=ModelConfigResponse)
async def get_model(model_id: str):
    """获取单个模型配置"""
    for m in model_store.load_models():
        if m.get("id") == model_id:
            return _to_response(m)
    raise HTTPException(status_code=404, detail="Model config not found")


@router.post("/", response_model=ModelConfigResponse)
async def create_model(model: ModelConfigCreate):
    """创建模型配置"""
    try:
        record = await model_store.save_model(model.model_dump())
        return _to_response(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{model_id}", response_model=ModelConfigResponse)
async def update_model(model_id: str, model: ModelConfigUpdate):
    """更新模型配置"""
    try:
        record = await model_store.save_model(
            model.model_dump(exclude_unset=True), model_id=model_id
        )
        # 配置已变更，清空服务实例池让下次取用重建
        from app.services.ai_service import clear_service_pool
        clear_service_pool()
        return _to_response(record)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LookupError:
        raise HTTPException(status_code=404, detail="Model config not found")


@router.delete("/{model_id}")
async def delete_model(model_id: str):
    """删除模型配置"""
    try:
        await model_store.delete_model(model_id)
        from app.services.ai_service import clear_service_pool
        clear_service_pool()
        return {"message": "Model config deleted successfully"}
    except LookupError:
        raise HTTPException(status_code=404, detail="Model config not found")


@router.post("/{model_id}/test")
async def test_model(model_id: str):
    """测试模型连通性"""
    target = None
    for m in model_store.load_models():
        if m.get("id") == model_id:
            target = m
            break
    if not target:
        raise HTTPException(status_code=404, detail="Model config not found")

    from app.services.ai_service import AIService

    service = AIService(
        api_key=target["api_key"],
        base_url=target.get("api_base") or None,
        model=target["model_name"],
    )
    ok = await service.test_connection()
    return {"success": ok, "message": "连接成功" if ok else "连接失败，请检查配置"}
