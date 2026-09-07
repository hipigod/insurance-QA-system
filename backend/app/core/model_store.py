"""
模型配置文件存储 - data/model_config.json
管理后台配置的模型统一落盘到此文件，作为唯一配置来源
"""
import asyncio
import json
import os
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from app.core.config import BASE_DIR

MODEL_CONFIG_FILE = BASE_DIR / "data" / "model_config.json"

# 进程内读写锁，避免并发写坏文件
_file_lock = asyncio.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _empty_store() -> Dict:
    return {"models": []}


def load_models() -> List[Dict]:
    """读取全部模型配置"""
    if not MODEL_CONFIG_FILE.exists():
        return []
    try:
        with open(MODEL_CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        models = data.get("models", [])
        if not isinstance(models, list):
            return []
        return models
    except (json.JSONDecodeError, OSError):
        # 文件损坏时不炸掉整个管理后台，返回空列表
        return []


def _atomic_write(data: Dict) -> None:
    """原子写入：先写临时文件再替换，避免写一半断电丢配置"""
    MODEL_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=str(MODEL_CONFIG_FILE.parent), suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, MODEL_CONFIG_FILE)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


def get_model_by_name(model_name: str) -> Optional[Dict]:
    """按模型名称查找"""
    for m in load_models():
        if m.get("model_name") == model_name:
            return m
    return None


async def save_model(model_data: Dict, model_id: Optional[str] = None) -> Dict:
    """
    新增或更新模型配置
    model_id 为空时新增（生成 uuid），否则按 id 更新
    """
    async with _file_lock:
        store = _empty_store()
        if MODEL_CONFIG_FILE.exists():
            try:
                with open(MODEL_CONFIG_FILE, "r", encoding="utf-8") as f:
                    store = json.load(f)
            except (json.JSONDecodeError, OSError):
                store = _empty_store()

        models: List[Dict] = store.get("models", [])
        now = _now_iso()

        if model_id is None:
            # 新增：名称查重
            if any(m.get("model_name") == model_data["model_name"] for m in models):
                raise ValueError("模型名称已存在")
            record = {
                "id": uuid.uuid4().hex[:8],
                "model_name": model_data["model_name"],
                "provider": model_data.get("provider") or "",
                "api_key": model_data["api_key"],
                "api_base": model_data.get("api_base") or "",
                "is_active": bool(model_data.get("is_active", True)),
                "created_at": now,
                "updated_at": now,
            }
            models.append(record)
        else:
            # 更新
            target = next((m for m in models if m.get("id") == model_id), None)
            if target is None:
                raise LookupError("模型配置不存在")
            # 若改名，名称查重
            new_name = model_data.get("model_name")
            if (
                new_name
                and new_name != target.get("model_name")
                and any(m.get("model_name") == new_name for m in models)
            ):
                raise ValueError("模型名称已存在")
            for key in ("model_name", "provider", "api_key", "api_base", "is_active"):
                if key in model_data and model_data[key] is not None:
                    target[key] = model_data[key]
            target["is_active"] = bool(target.get("is_active"))
            target["updated_at"] = now
            record = target

        store["models"] = models
        _atomic_write(store)
        return record


async def delete_model(model_id: str) -> None:
    """删除模型配置"""
    async with _file_lock:
        if not MODEL_CONFIG_FILE.exists():
            return
        try:
            with open(MODEL_CONFIG_FILE, "r", encoding="utf-8") as f:
                store = json.load(f)
        except (json.JSONDecodeError, OSError):
            return

        models = [m for m in store.get("models", []) if m.get("id") != model_id]
        if len(models) == len(store.get("models", [])):
            raise LookupError("模型配置不存在")

        store["models"] = models
        _atomic_write(store)


async def migrate_from_db_if_needed() -> int:
    """
    启动时一次性迁移：把数据库 model_configs 表里的旧配置导入 JSON
    仅在 JSON 文件不存在时执行，避免覆盖新配置
    返回迁移条数
    """
    if MODEL_CONFIG_FILE.exists():
        return 0

    try:
        from sqlalchemy import select
        from app.core.database import AsyncSessionLocal
        from app.models.models import ModelConfig
    except ImportError:
        return 0

    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(ModelConfig))
            rows = result.scalars().all()
            if not rows:
                return 0

            store = _empty_store()
            now = _now_iso()
            for r in rows:
                store["models"].append({
                    "id": uuid.uuid4().hex[:8],
                    "model_name": r.model_name,
                    "provider": r.provider or "",
                    "api_key": r.api_key or "",
                    "api_base": r.api_base or "",
                    "is_active": bool(r.is_active),
                    "created_at": now,
                    "updated_at": now,
                })
            async with _file_lock:
                _atomic_write(store)
            return len(rows)
    except Exception as e:
        print(f"[WARN] 模型配置迁移失败（不影响启动）: {e}")
        return 0
