"""
WebSocket服务 - 管理对话会话
"""
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from app.models.schemas import ChatMessage


class DialogueSession:
    """对话会话类"""

    def __init__(
        self,
        role_id: int,
        product_id: int,
        role_data: dict = None,
        product_data: dict = None
    ):
        self.session_id = str(uuid.uuid4())
        self.role_id = role_id
        self.product_id = product_id
        self.role_data = role_data or {}  # 存储角色完整信息
        self.product_data = product_data or {}  # 存储产品完整信息
        self.dialogue_history: List[ChatMessage] = []
        self.created_at = datetime.now()
        self.is_active = True

    def add_message(self, role: str, content: str):
        """添加消息到历史"""
        message = ChatMessage(role=role, content=content)
        self.dialogue_history.append(message)
        return message

    def end_session(self):
        """结束会话"""
        self.is_active = False


class WebSocketManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # 存储所有活动会话: {session_id: DialogueSession}
        self.active_sessions: Dict[str, DialogueSession] = {}
        # 存储WebSocket连接: {session_id: websocket}
        self.active_connections: Dict[str, any] = {}

    async def create_session(
        self,
        role_id: int,
        product_id: int,
        role_data: dict = None,
        product_data: dict = None
    ) -> DialogueSession:
        """创建新会话"""
        session = DialogueSession(role_id, product_id, role_data, product_data)
        self.active_sessions[session.session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[DialogueSession]:
        """获取会话"""
        return self.active_sessions.get(session_id)

    def end_session(self, session_id: str):
        """结束会话"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id].end_session()

    def remove_session(self, session_id: str):
        """移除会话"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        if session_id in self.active_connections:
            del self.active_connections[session_id]


# 全局WebSocket管理器
websocket_manager = WebSocketManager()
