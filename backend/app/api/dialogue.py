"""
对话相关API - WebSocket实时通信
模型在开始对话时选定，绑定到会话
"""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.core.database import get_db, AsyncSessionLocal
from app.core import model_store
from app.models.models import CustomerRole, InsuranceProduct, ScoringDimension, ExcellentCase, PracticeRecord
from app.models.schemas import DialogueStartRequest, ScoringRequest
from app.services.ai_service import get_ai_service_by_name
from app.services.websocket_service import websocket_manager

router = APIRouter(prefix="/dialogue", tags=["对话"])


async def _save_practice_record(session, score_result: dict):
    """评分完成后把练习记录落库，失败不影响返回评分"""
    try:
        db = AsyncSessionLocal()
        try:
            record = PracticeRecord(
                role_id=session.role_id,
                product_id=session.product_id,
                dialogue_data=[
                    {"role": m.role, "content": m.content}
                    for m in session.dialogue_history
                ],
                score_data=score_result,
                total_score=score_result.get("total_score"),
            )
            db.add(record)
            await db.commit()
        finally:
            await db.close()
    except Exception as e:
        print(f"[ERROR] 练习记录保存失败: {e}")


def _resolve_model_service(model_name: str = None):
    """按名称取启用的模型服务；未指定名称时取第一个启用中的模型"""
    if model_name:
        return get_ai_service_by_name(model_name)
    models = model_store.load_models()
    for m in models:
        if m.get("is_active"):
            return get_ai_service_by_name(m["model_name"])
    raise ValueError("尚未配置任何启用的模型，请先在管理后台添加")


@router.post("/start")
async def start_dialogue(
    request: DialogueStartRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    开始对话 - 创建会话并获取AI首次回复
    """
    # 模型校验最前：纯文件读，配置错误时给出最准确的报错
    try:
        ai_service = _resolve_model_service(request.model_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 获取角色信息
    role_result = await db.execute(select(CustomerRole).where(CustomerRole.id == request.role_id))
    role = role_result.scalar_one_or_none()

    if not role:
        raise HTTPException(status_code=404, detail="角色不存在")

    # 获取产品信息
    product_result = await db.execute(select(InsuranceProduct).where(InsuranceProduct.id == request.product_id))
    product = product_result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="产品不存在")

    # 构建角色和产品数据字典
    role_data = {
        "id": role.id,
        "name": role.name,
        "system_prompt": role.system_prompt
    }

    product_data = {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "coverage": product.coverage,
        "premium_range": product.premium_range,
        "target_audience": product.target_audience,
        "detailed_info": product.detailed_info
    }

    # 创建会话并保存角色和产品数据
    session = await websocket_manager.create_session(
        request.role_id,
        request.product_id,
        role_data,
        product_data
    )
    # 会话绑定模型，后续WebSocket与评分都用它
    session.ai_service = ai_service
    session.model_name = ai_service.model

    # 构建产品信息文本
    product_info = f"""产品名称：{product.name}
产品类型：{product.product_type}
产品简介：{product.description}
保障范围：{product.coverage}
保费范围：{product.premium_range}
适用人群：{product.target_audience}"""

    # 生成AI首次问候
    try:
        greeting = await ai_service.generate_dialogue_response(
            role_prompt=role.system_prompt,
            product_info=product_info,
            dialogue_history=[],
            user_message=""  # 首次对话，无用户消息
        )

        # 记录AI回复
        session.add_message("assistant", greeting)

        return {
            "session_id": session.session_id,
            "greeting": greeting,
            "role_name": role.name,
            "product_name": product.name
        }

    except Exception as e:
        websocket_manager.remove_session(session.session_id)
        raise HTTPException(status_code=500, detail=f"AI服务异常: {str(e)}")


@router.websocket("/ws/{session_id}")
async def websocket_dialogue(websocket: WebSocket, session_id: str):
    """
    WebSocket实时对话接口
    """
    await websocket.accept()

    # 获取会话
    session = websocket_manager.get_session(session_id)
    if not session:
        await websocket.close(code=4000, reason="会话不存在")
        return

    websocket_manager.active_connections[session_id] = websocket

    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_text()
            message_data = json.loads(data)

            user_message = message_data.get("message", "")
            action = message_data.get("action", "chat")

            # 处理不同动作
            if action == "chat":
                # 记录用户消息
                session.add_message("user", user_message)

                # 发送"正在输入"状态
                await websocket.send_json({
                    "type": "status",
                    "status": "thinking"
                })

                # 获取角色和产品信息（从会话中获取）
                role_prompt = session.role_data.get("system_prompt", "")
                product_info = f"""产品名称：{session.product_data.get("name")}
产品简介：{session.product_data.get("description")}
保障范围：{session.product_data.get("coverage")}
保费范围：{session.product_data.get("premium_range")}"""

                # 生成AI回复
                try:
                    ai_reply = await session.ai_service.generate_dialogue_response(
                        role_prompt=role_prompt,
                        product_info=product_info,
                        dialogue_history=session.dialogue_history,
                        user_message=user_message
                    )

                    # 记录AI回复
                    session.add_message("assistant", ai_reply)

                    # 发送AI回复
                    await websocket.send_json({
                        "type": "message",
                        "role": "assistant",
                        "content": ai_reply
                    })

                except Exception as e:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"AI服务异常: {str(e)}"
                    })

            elif action == "end":
                # 结束对话，触发评分
                print(f"[DEBUG] 收到结束对话请求, session_id={session_id}")
                print(f"[DEBUG] 对话轮数: {len(session.dialogue_history)}")

                await websocket.send_json({
                    "type": "status",
                    "status": "scoring"
                })

                # 调用评分服务
                try:
                    print("[DEBUG] 开始AI评分流程...")

                    # 从数据库获取评分维度配置
                    db = AsyncSessionLocal()
                    try:
                        dimensions_result = await db.execute(select(ScoringDimension))
                        dimensions = dimensions_result.scalars().all()

                        # 构建评分维度配置
                        scoring_dimensions = {}
                        for dim in dimensions:
                            scoring_dimensions[dim.name] = {
                                "weight": dim.weight,
                                "prompt": dim.evaluation_prompt or dim.description
                            }
                        print(f"[DEBUG] 加载了{len(dimensions)}个评分维度")
                    finally:
                        await db.close()

                    # 构建对话文本
                    dialogue_text = "\n".join([
                        f"{msg.role}: {msg.content}"
                        for msg in session.dialogue_history
                    ])
                    print(f"[DEBUG] 对话文本长度: {len(dialogue_text)}字符")

                    # 调用AI评分（使用会话绑定的模型）
                    print("[DEBUG] 调用AI评分服务...")
                    score_result = await session.ai_service.generate_scoring(
                        dialogue_text=dialogue_text,
                        role_name=session.role_data.get("name", ""),
                        product_name=session.product_data.get("name", ""),
                        scoring_dimensions=scoring_dimensions,
                        scoring_prompt=""
                    )

                    print(f"[DEBUG] AI评分完成, 总分: {score_result.get('total_score', 'N/A')}")
                    print(f"[DEBUG] 发送评分结果到前端...")

                    # 发送评分结果
                    await websocket.send_json({
                        "type": "score",
                        "data": score_result
                    })

                    # 练习记录落库
                    await _save_practice_record(session, score_result)

                    print("[DEBUG] 评分结果已发送")

                except Exception as e:
                    print(f"[ERROR] 评分失败: {str(e)}")
                    import traceback
                    traceback.print_exc()

                    await websocket.send_json({
                        "type": "error",
                        "message": f"评分失败: {str(e)}"
                    })

                break

    except WebSocketDisconnect:
        print(f"WebSocket断开: {session_id}")
    except Exception as e:
        print(f"WebSocket错误: {str(e)}")
        await websocket.close(code=4001, reason=f"服务器错误: {str(e)}")
    finally:
        websocket_manager.remove_session(session_id)


@router.post("/score")
async def score_dialogue(
    request: ScoringRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    对话评分接口 (HTTP方式，WebSocket失败时的备用方案)
    """
    # 获取评分维度
    dimensions_result = await db.execute(select(ScoringDimension))
    dimensions = dimensions_result.scalars().all()

    # 构建评分维度配置
    scoring_dimensions = {}
    for dim in dimensions:
        scoring_dimensions[dim.name] = {
            "weight": dim.weight,
            "prompt": dim.evaluation_prompt or dim.description
        }

    # 获取角色和产品信息
    role_result = await db.execute(select(CustomerRole).where(CustomerRole.id == request.role_id))
    role = role_result.scalar_one_or_none()

    product_result = await db.execute(select(InsuranceProduct).where(InsuranceProduct.id == request.product_id))
    product = product_result.scalar_one_or_none()

    # 构建对话文本
    dialogue_text = "\n".join([
        f"{msg.role}: {msg.content}" for msg in request.dialogue_history
    ])

    try:
        # 备用评分通道：优先取会话绑定的模型，会话已失效则回退第一个启用模型
        session = websocket_manager.get_session(request.session_id)
        if session and getattr(session, "ai_service", None):
            ai_service = session.ai_service
        else:
            ai_service = _resolve_model_service(None)
        score_result = await ai_service.generate_scoring(
            dialogue_text=dialogue_text,
            role_name=role.name if role else "",
            product_name=product.name if product else "",
            scoring_dimensions=scoring_dimensions,
            scoring_prompt=""
        )

        # 练习记录落库（会话存在时）
        if session:
            await _save_practice_record(session, score_result)

        return score_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评分失败: {str(e)}")


@router.get("/records")
async def get_practice_records(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """练习记录列表（倒序，带角色和产品名称）"""
    from sqlalchemy import func

    records_result = await db.execute(
        select(PracticeRecord)
        .order_by(PracticeRecord.created_at.desc(), PracticeRecord.id.desc())
        .offset(offset)
        .limit(limit)
    )
    records = records_result.scalars().all()

    # 关联名称映射
    roles_result = await db.execute(select(CustomerRole))
    products_result = await db.execute(select(InsuranceProduct))
    role_names = {r.id: r.name for r in roles_result.scalars().all()}
    product_names = {p.id: p.name for p in products_result.scalars().all()}

    total_result = await db.execute(select(func.count(PracticeRecord.id)))
    total = total_result.scalar() or 0

    return {
        "total": total,
        "items": [
            {
                "id": r.id,
                "role_id": r.role_id,
                "product_id": r.product_id,
                "role_name": role_names.get(r.role_id, f"角色#{r.role_id}"),
                "product_name": product_names.get(r.product_id, f"产品#{r.product_id}"),
                "total_score": r.total_score,
                "dialogue_data": r.dialogue_data or [],
                "score_data": r.score_data or {},
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in records
        ],
    }


@router.delete("/records")
async def clear_practice_records(db: AsyncSession = Depends(get_db)):
    """清空全部练习记录"""
    await db.execute(delete(PracticeRecord))
    await db.commit()
    return {"message": "练习记录已清空"}
