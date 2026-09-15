"""
AI模型服务 - 处理与大模型的交互
模型配置来自 data/model_config.json（管理后台维护）
"""
import json
import asyncio
from typing import List, Dict
from openai import AsyncOpenAI
from app.core.config import settings
from app.models.schemas import ChatMessage


class AIService:
    """AI服务类 - 按传入的模型配置实例化，支持多模型并存"""

    def __init__(self, api_key: str, base_url: str = None, model: str = None):
        """
        初始化AI服务

        Args:
            api_key: API密钥（必填）
            base_url: API基础URL（兼容OpenAI协议的接口地址）
            model: 模型名称
        """
        if not api_key:
            raise ValueError("API Key未配置")
        if not model:
            raise ValueError("模型名称未配置")

        self.api_key = api_key
        self.base_url = base_url or "https://api.openai.com/v1"
        self.model = model

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
1. 完全沉浸在角色中，像真人一样有情绪起伏：好奇、困惑、不耐烦、失望、生气都要通过语气和用词表现出来
2. 有自己的喜好和厌恶，对喜欢的解释方式给予积极回应，对厌恶的沟通方式表达不满
3. 根据销售人员的回应做出符合角色性格的合理反应，销售答得好就松动，答得差就反感
4. 回复长度控制在50-150字，口语化，可以用语气词（啊、哦、唉、行吧）
5. 不要直接重复之前说过的内容
6. 严格遵循角色设定中的【耐心与挂断规则】：当敷衍次数累计达到上限时，你会果断结束对话，最后一句话表达失望或愤怒，并在回复末尾加上【挂断】标记"""
            }
        ]

        # 添加历史对话
        # 全量历史：角色情绪与耐心计数需要完整上下文才能延续，
        # 截断会导致客户的挂断进度失忆（对话上限20轮，上下文预算充足）
        for msg in dialogue_history:
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

        prompt = f"""你是一个专业的保险销售培训师，负责严格评估销售人员的对话表现。你是严厉的考官，绝不送分。

【评分维度与权重】
{dimensions_desc}

【对话信息】
角色类型：{role_name}
保险产品：{product_name}

【完整对话记录】
{dialogue_text}

【评分标准（严格执行，对号入座）】
每个维度按以下档位定档，先定档再在档位区间内微调：
- 90-100 卓越：该维度行为完整出现且有亮点（如主动深挖需求并确认、用通俗类比讲清条款、化解异议后促成签单）
- 75-89 良好：该维度核心行为基本做到，有小瑕疵
- 60-74 及格：该维度仅部分做到，生硬或有遗漏
- 30-59 差：该维度行为缺失或敷衍（如需求挖掘只问一句就推销、异议处理只重复话术）
- 0-29 极差：该维度行为完全缺失、答非所问、编造产品信息、或被客户挂断

【一票否决项】
- 销售人员出现编造产品保障/费率、承诺"肯定赔"等误导陈述：相关维度直接0-20分
- 客户明确表达不满或挂断：促成能力维度不高于30分
- 对话中销售只顾推销、完全无视客户问题和情绪：需求挖掘不高于30分

【评分要求】
1. 每个维度独立打分（0-100分），必须与对话中的实际证据对应，评价中引用对话原文片段佐证
2. 给出每个维度的具体评价（50字左右），没做到的明确说没做到
3. 识别客户提出的异议类型标签（价格异议、信任异议、需求异议、竞品异议等）
4. 生成总体评价（200-300字），包括：优点分析（2-3点）、待改进点（2-3点）、具体改进建议
5. 宁低勿高：表现平庸就给及格档，只有真正出色的表现才配75分以上

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
                    max_tokens=8000  # 推理型模型思考也计入token，给足余量
                ),
                timeout=120  # 推理型模型评分耗时更长
            )

            message = response.choices[0].message
            finish_reason = response.choices[0].finish_reason
            result_text = message.content or ""

            # 推理型模型content为空：思考耗尽token或未产出最终答案
            if not result_text.strip():
                reasoning = getattr(message, "reasoning_content", None)
                if reasoning:
                    raise Exception(
                        "该模型为推理型，思考内容耗尽了输出额度未返回评分结果。"
                        "请在管理后台换非推理模型，或缩短对话后重试"
                    )
                if finish_reason == "length":
                    raise Exception("AI输出被截断（finish_reason=length），请重试或更换模型")
                raise Exception("AI返回了空内容，请重试或更换模型")

            result = self._extract_json(result_text)
            if result is None:
                raise Exception("AI返回中未找到有效的JSON评分结果（返回内容前200字: "
                                + result_text[:200].replace("\n", " ") + "）")

            # 将中文key转换为英文key,以匹配前端期望
            converted_result = self._convert_score_keys(result)
            return converted_result

        except asyncio.TimeoutError:
            raise Exception("评分超时，推理型模型响应较慢，请稍后重试或更换非推理模型")
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {result_text[:500]}")
            raise Exception(f"AI返回格式错误: {str(e)}")
        except Exception as e:
            if str(e).startswith(("AI返回", "该模型", "评分超时")):
                raise
            print(f"评分失败: {str(e)}")
            raise Exception(f"评分服务异常: {str(e)}")

    def _extract_json(self, text: str):
        """
        从AI回复中稳健提取JSON对象
        优先取```代码块内容，否则取最外层大括号之间的部分
        """
        import re
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if m:
            text = m.group(1).strip()
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end <= start:
            return None
        candidate = text[start:end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None

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


# 按模型名称缓存的AI服务实例池: {model_name: AIService}
_service_pool: Dict[str, AIService] = {}


def get_ai_service_by_name(model_name: str) -> AIService:
    """
    按模型名称获取AI服务实例
    配置文件中不存在该模型或未启用时抛异常
    """
    from app.core import model_store

    cached = _service_pool.get(model_name)
    if cached is not None:
        return cached

    config = model_store.get_model_by_name(model_name)
    if config is None:
        raise ValueError(f"模型配置不存在: {model_name}")
    if not config.get("is_active"):
        raise ValueError(f"模型已禁用: {model_name}")

    service = AIService(
        api_key=config["api_key"],
        base_url=config.get("api_base") or None,
        model=config["model_name"],
    )
    _service_pool[model_name] = service
    return service


def clear_service_pool():
    """清空服务实例池（模型配置变更后调用，下次取用时重建）"""
    _service_pool.clear()
