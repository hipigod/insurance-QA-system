"""
对话相关API - WebSocket实时通信
"""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import CustomerRole, InsuranceProduct, PracticeRecord
from app.models.schemas import DialogueStartRequest, ChatMessage, ScoringRequest
from app.services.ai_service import get_ai_service
from app.services.websocket_service import websocket_manager
from typing import Dict

router = APIRouter(prefix="/dialogue", tags=["对话"])


@router.post("/start")
async def start_dialogue(
    request: DialogueStartRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    开始对话 - 创建会话并获取AI首次回复
    """
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

    # 创建会话
    session = await websocket_manager.create_session(request.role_id, request.product_id)

    # 构建产品信息文本
    product_info = f"""产品名称：{product.name}
产品类型：{product.product_type}
产品简介：{product.description}
保障范围：{product.coverage}
保费范围：{product.premium_range}
适用人群：{product.target_audience}"""

    # 生成AI首次问候
    try:
        ai_service = get_ai_service()
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

                # 获取角色和产品信息
                # TODO: 从数据库获取，这里暂时用缓存

                # 生成AI回复
                try:
                    ai_service = get_ai_service()
                    ai_reply = await ai_service.generate_dialogue_response(
                        role_prompt="",  # TODO: 从缓存获取
                        product_info="",  # TODO: 从缓存获取
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
                await websocket.send_json({
                    "type": "status",
                    "status": "scoring"
                })

                # TODO: 调用评分服务
                await websocket.send_json({
                    "type": "score",
                    "data": {
                        "total_score": 85,
                        "message": "评分完成"
                    }
                })

                break

    except WebSocketDisconnect:
        print(f"WebSocket断开: {session_id}")
    finally:
        websocket_manager.remove_session(session_id)


@router.post("/score")
async def score_dialogue(
    request: ScoringRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    对话评分接口
    """
    # 获取会话
    session = websocket_manager.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")

    # 获取角色和产品信息
    role_result = await db.execute(select(CustomerRole).where(CustomerRole.id == request.role_id))
    role = role_result.scalar_one_or_none()

    product_result = await db.execute(select(InsuranceProduct).where(InsuranceProduct.id == request.product_id))
    product = product_result.scalar_one_or_none()

    # 构建对话文本
    dialogue_text = "\n".join([
        f"{msg.role}: {msg.content}" for msg in request.dialogue_history
    ])

    # 获取评分维度
    # TODO: 从数据库获取评分维度配置

    try:
        ai_service = get_ai_service()
        score_result = await ai_service.generate_scoring(
            dialogue_text=dialogue_text,
            role_name=role.name if role else "",
            product_name=product.name if product else "",
            scoring_dimensions={
                "沟通能力": {"weight": 25, "prompt": "..."},
                "有效营销": {"weight": 25, "prompt": "..."},
                "产品熟练度": {"weight": 25, "prompt": "..."},
                "异议处理能力": {"weight": 25, "prompt": "..."}
            },
            scoring_prompt=""
        )

        # 保存练习记录
        # TODO: 保存到数据库

        return score_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评分失败: {str(e)}")
