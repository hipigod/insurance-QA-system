"""
Pydantic数据模型定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== 客户角色相关 ==========
class RoleBase(BaseModel):
    """角色基础模型"""
    name: str = Field(..., description="角色名称")
    description: Optional[str] = Field(None, description="角色简介")
    difficulty: Optional[str] = Field("普通", description="难度等级")
    system_prompt: str = Field(..., description="角色提示词")


class RoleCreate(RoleBase):
    """创建角色"""
    pass


class RoleUpdate(BaseModel):
    """更新角色"""
    name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    system_prompt: Optional[str] = None


class RoleResponse(RoleBase):
    """角色响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 保险产品相关 ==========
class ProductBase(BaseModel):
    """产品基础模型"""
    name: str = Field(..., description="产品名称")
    description: Optional[str] = Field(None, description="产品简介")
    product_type: Optional[str] = Field(None, description="产品类型")
    coverage: Optional[str] = Field(None, description="保障范围")
    premium_range: Optional[str] = Field(None, description="保费范围")
    target_audience: Optional[str] = Field(None, description="适用人群")
    detailed_info: Optional[str] = Field(None, description="产品详细信息")


class ProductCreate(ProductBase):
    """创建产品"""
    pass


class ProductUpdate(BaseModel):
    """更新产品"""
    name: Optional[str] = None
    description: Optional[str] = None
    product_type: Optional[str] = None
    coverage: Optional[str] = None
    premium_range: Optional[str] = None
    target_audience: Optional[str] = None
    detailed_info: Optional[str] = None


class ProductResponse(ProductBase):
    """产品响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 对话相关 ==========
class ChatMessage(BaseModel):
    """聊天消息"""
    role: str = Field(..., description="角色: user/assistant/system")
    content: str = Field(..., description="消息内容")


class DialogueStartRequest(BaseModel):
    """开始对话请求"""
    role_id: int = Field(..., description="客户角色ID")
    product_id: int = Field(..., description="保险产品ID")


class DialogueMessage(BaseModel):
    """对话消息"""
    session_id: str = Field(..., description="会话ID")
    message: str = Field(..., description="用户消息")


class DialogueResponse(BaseModel):
    """对话响应"""
    reply: str = Field(..., description="AI回复")
    is_end: bool = Field(False, description="是否结束")


# ========== 评分相关 ==========
class DimensionScore(BaseModel):
    """维度评分"""
    score: int = Field(..., ge=0, le=100, description="分数(0-100)")
    evaluation: str = Field(..., description="评价文本")


class ScoreDetail(BaseModel):
    """评分详情"""
    dimension: str = Field(..., description="维度名称")
    score: int
    evaluation: str


class ScoringRequest(BaseModel):
    """评分请求"""
    session_id: str = Field(..., description="会话ID")
    dialogue_history: List[ChatMessage] = Field(..., description="对话历史")
    role_id: int = Field(..., description="角色ID")
    product_id: int = Field(..., description="产品ID")


class ScoringResponse(BaseModel):
    """评分响应"""
    total_score: int = Field(..., ge=0, le=100, description="总分(0-100)")
    dimension_scores: Dict[str, DimensionScore] = Field(..., description="各维度评分")
    objection_tags: List[str] = Field(default_factory=list, description="异议类型标签")
    excellent_cases: List[Dict[str, str]] = Field(default_factory=list, description="优秀案例对比")
    overall_evaluation: str = Field(..., description="总体评价")
    dialogue_nodes: Optional[Dict[str, str]] = Field(None, description="关键节点点评")


class PracticeRecordResponse(BaseModel):
    """练习记录响应"""
    id: int
    role_id: int
    product_id: int
    total_score: int
    dialogue_data: List[ChatMessage]
    score_data: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 评分标准配置相关 ==========
class ScoringDimensionBase(BaseModel):
    """评分维度基础模型"""
    name: str = Field(..., description="维度名称")
    description: Optional[str] = Field(None, description="维度描述")
    weight: float = Field(25.0, ge=0, le=100, description="权重")
    evaluation_prompt: Optional[str] = Field(None, description="评分依据提示词")


class ScoringDimensionCreate(ScoringDimensionBase):
    """创建评分维度"""
    pass


class ScoringDimensionUpdate(BaseModel):
    """更新评分维度"""
    name: Optional[str] = None
    description: Optional[str] = None
    weight: Optional[float] = None
    evaluation_prompt: Optional[str] = None


class ScoringDimensionResponse(ScoringDimensionBase):
    """评分维度响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 模型配置相关 ==========
class ModelConfigBase(BaseModel):
    """模型配置基础模型"""
    model_name: str = Field(..., description="模型名称")
    provider: Optional[str] = Field(None, description="提供商")
    api_key: str = Field(..., description="API Key")
    api_base: Optional[str] = Field(None, description="API Base URL")


class ModelConfigCreate(ModelConfigBase):
    """创建模型配置"""
    pass


class ModelConfigUpdate(BaseModel):
    """更新模型配置"""
    model_name: Optional[str] = None
    provider: Optional[str] = None
    api_key: Optional[str] = None
    api_base: Optional[str] = None


class ModelConfigResponse(BaseModel):
    """模型配置响应"""
    id: int
    model_name: str
    provider: Optional[str]
    is_active: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 优秀案例相关 ==========
class ExcellentCaseBase(BaseModel):
    """优秀案例基础模型"""
    weakness_type: str = Field(..., description="薄弱环节类型")
    case_content: str = Field(..., description="案例内容")
    dialogue_node: Optional[str] = Field(None, description="对应对话节点")


class ExcellentCaseCreate(ExcellentCaseBase):
    """创建优秀案例"""
    pass


class ExcellentCaseResponse(ExcellentCaseBase):
    """优秀案例响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== 通用响应 ==========
class ResponseModel(BaseModel):
    """通用响应模型"""
    code: int = Field(200, description="状态码")
    message: str = Field("success", description="消息")
    data: Optional[Any] = Field(None, description="数据")
