"""
添加模型配置到数据库
"""
import asyncio
import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.models.models import ModelConfig


async def add_qwen_model():
    """添加通义千问模型配置"""
    print("=" * 60)
    print("添加通义千问模型配置")
    print("=" * 60)

    async with AsyncSessionLocal() as session:
        # 检查是否已存在
        from sqlalchemy import select
        result = await session.execute(
            select(ModelConfig).where(ModelConfig.model_name == "qwen-plus")
        )
        existing = result.scalar_one_or_none()

        if existing:
            print("[INFO] qwen-plus模型配置已存在,更新中...")
            existing.provider = "通义千问"
            existing.api_key = "sk-8b1831a371984c6483b413a759463619"
            existing.api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
            existing.is_active = True
            await session.commit()
            print("[OK] qwen-plus模型配置更新成功")
        else:
            # 取消其他模型的激活状态
            await session.execute(
                select(ModelConfig).where(ModelConfig.is_active == True)
            )
            # 创建新模型配置
            model = ModelConfig(
                model_name="qwen-plus",
                provider="通义千问",
                api_key="sk-8b1831a371984c6483b413a759463619",
                api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
                is_active=True
            )
            session.add(model)
            await session.commit()
            print("[OK] qwen-plus模型配置添加成功")

        # 显示所有模型配置
        print("\n当前模型配置列表:")
        result = await session.execute(select(ModelConfig))
        models = result.scalars().all()

        for m in models:
            status = "✓ 已激活" if m.is_active else "  未激活"
            print(f"  [{m.id}] {m.model_name} ({m.provider}) {status}")

    print("\n" + "=" * 60)
    print("[OK] 模型配置完成!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(add_qwen_model())
