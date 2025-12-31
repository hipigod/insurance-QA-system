"""
AI模型服务 - 处理与大模型的交互
"""
import json
import asyncio
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.schemas import ChatMessage


class AIService:
    """AI服务类"""

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model: str = None
    ):
        """
        初始化AI服务

        Args:
            api_key: API密钥
            base_url: API基础URL
            model: 模型名称
        """
        self.api_key = api_key or settings.MODEL_API_KEY
        self.base_url = base_url or settings.MODEL_API_BASE
        self.model = model or settings.DEFAULT_MODEL

        if not self.api_key:
            raise ValueError("API Key未配置")

        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    async def generate_dialogue_response(
        self,
        role_prompt: str,
        product_info: str,
        dialogue_history: List[ChatMessage],
        user_message: str
    ) -> str:
        """
        生成对话回复

        Args:
            role_prompt: 角色提示词
            product_info: 产品信息
            dialogue_history: 对话历史
            user_message: 用户消息

        Returns:
            AI回复文本
        """
        # 构建对话历史
        messages = [
            {
                "role": "system",
                "content": f"""你是一个保险客户模拟角色，用于帮助保险销售人员练习沟通技巧。

【角色设定】
{role_prompt}

【当前产品信息】
产品名称：{product_info}

【注意事项】
1. 始终保持角色性格特征
2. 根据销售人员的回应做出合理的反应
3. 自然地提出各种客户异议（价格、信任、需求等）
4. 回复长度控制在50-150字
5. 不要直接重复之前说过的内容"""
            }
        ]

        # 添加历史对话
        for msg in dialogue_history[-5:]:  # 只保留最近5轮对话
            if msg.role != "system":
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })

        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            # 调用大模型
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=settings.AI_TEMPERATURE,
                    max_tokens=500
                ),
                timeout=settings.AI_RESPONSE_TIMEOUT
            )

            return response.choices[0].message.content

        except asyncio.TimeoutError:
            return "抱歉，响应超时。请重新发送消息，或者稍后再试。"
        except Exception as e:
            print(f"AI调用失败: {str(e)}")
            return "抱歉，我现在无法回应。请稍后再试，或者结束本次对话。"

    async def generate_scoring(
        self,
        dialogue_text: str,
        role_name: str,
        product_name: str,
        scoring_dimensions: Dict[str, Dict],
        scoring_prompt: str
    ) -> Dict:
        """
        生成评分

        Args:
            dialogue_text: 完整对话文本
            role_name: 角色名称
            product_name: 产品名称
            scoring_dimensions: 评分维度配置
            scoring_prompt: 评分提示词

        Returns:
            评分结果字典
        """
        # 构建评分维度描述
        dimensions_desc = "\n".join([
            f"维度{i+1}：{name}（权重{config['weight']}%）\n{config.get('prompt', '')}"
            for i, (name, config) in enumerate(scoring_dimensions.items())
        ])

        prompt = f"""你是一个专业的保险销售培训师，负责评估销售人员的对话表现。

【评分维度与权重】
{dimensions_desc}

【对话信息】
角色类型：{role_name}
保险产品：{product_name}

【完整对话记录】
{dialogue_text}

【评分要求】
1. 每个维度独立打分（0-100分）
2. 给出每个维度的具体评价（50字左右）
3. 识别客户提出的异议类型标签（价格异议、信任异议、需求异议、竞品异议等）
4. 生成总体评价（200-300字），包括：优点分析（2-3点）、待改进点（2-3点）、具体改进建议

{scoring_prompt}

【输出格式】
请严格按照以下JSON格式输出，不要有任何其他内容：

{{
  "总分": 85,
  "维度评分": {{
    "沟通能力": {{
      "分数": 88,
      "评价": "表达清晰流畅，善于倾听客户需求..."
    }}
  }},
  "异议类型标签": ["价格异议", "信任异议"],
  "总体评价": "【优点】\\n1. ...\\n\\n【待改进】\\n1. ...\\n\\n【建议】\\n..."
}}
"""

        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "你是一个专业的保险销售培训师，负责评估销售人员的对话表现。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,  # 评分时降低温度，提高稳定性
                    max_tokens=2000
                ),
                timeout=15
            )

            result_text = response.choices[0].message.content

            # 解析JSON
            # 尝试提取JSON部分
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()

            result = json.loads(result_text)

            # 将中文key转换为英文key,以匹配前端期望
            converted_result = self._convert_score_keys(result)
            return converted_result

        except asyncio.TimeoutError:
            raise Exception("评分超时")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {result_text}")
            raise Exception(f"AI返回格式错误: {str(e)}")
        except Exception as e:
            print(f"评分失败: {str(e)}")
            raise Exception(f"评分服务异常: {str(e)}")

    def _convert_score_keys(self, result: Dict) -> Dict:
        """
        将AI返回的中文key转换为前端期望的英文key

        Args:
            result: AI返回的原始结果

        Returns:
            转换后的结果
        """
        converted = {}

        # 转换顶级key
        key_mapping = {
            "总分": "total_score",
            "维度评分": "dimension_scores",
            "异议类型标签": "objection_tags",
            "总体评价": "overall_evaluation"
        }

        for chinese_key, value in result.items():
            english_key = key_mapping.get(chinese_key, chinese_key)

            if chinese_key == "维度评分" and isinstance(value, dict):
                # 转换维度评分中的嵌套key
                converted[english_key] = {}
                for dim_name, dim_data in value.items():
                    if isinstance(dim_data, dict):
                        converted_dim = {}
                        dim_key_mapping = {
                            "分数": "score",
                            "评价": "evaluation"
                        }
                        for cn_key, cn_value in dim_data.items():
                            en_key = dim_key_mapping.get(cn_key, cn_key)
                            converted_dim[en_key] = cn_value
                        converted[english_key][dim_name] = converted_dim
                    else:
                        converted[english_key][dim_name] = dim_data
            else:
                converted[english_key] = value

        return converted

    async def test_connection(self) -> bool:
        """测试模型连接"""
        try:
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": "测试"}],
                    max_tokens=10
                ),
                timeout=5
            )
            return True
        except Exception as e:
            print(f"连接测试失败: {str(e)}")
            return False


# 全局AI服务实例
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """获取AI服务实例"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service


def reset_ai_service(api_key: str = None, base_url: str = None, model: str = None):
    """重置AI服务实例"""
    global _ai_service
    _ai_service = AIService(api_key=api_key, base_url=base_url, model=model)
