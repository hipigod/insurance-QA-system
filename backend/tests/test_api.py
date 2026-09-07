"""
自动化测试脚本 - 测试核心API功能
"""
import asyncio
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.core.database import AsyncSessionLocal, init_db
from app.models.models import CustomerRole, InsuranceProduct, ScoringDimension
from sqlalchemy import select
from app.services.ai_service import AIService


class TestResult:
    """测试结果类"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, test_name):
        self.passed += 1
        print(f"[PASS] {test_name}")

    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"[FAIL] {test_name}")
        print(f"   错误: {error}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"测试结果: {self.passed}/{total} 通过")
        if self.failed > 0:
            print(f"\n失败的测试:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        print(f"{'='*50}")
        return self.failed == 0


async def test_database_init(result: TestResult):
    """测试1: 数据库初始化"""
    try:
        await init_db()

        async with AsyncSessionLocal() as db:
            # 检查角色表
            roles_result = await db.execute(select(CustomerRole))
            roles = roles_result.scalars().all()

            if len(roles) >= 4:
                result.add_pass("TC001: 数据库初始化 - 角色数据")
            else:
                result.add_fail("TC001: 数据库初始化 - 角色数据", f"预期>=4个, 实际{len(roles)}个")

            # 检查产品表
            products_result = await db.execute(select(InsuranceProduct))
            products = products_result.scalars().all()

            if len(products) >= 3:
                result.add_pass("TC002: 数据库初始化 - 产品数据")
            else:
                result.add_fail("TC002: 数据库初始化 - 产品数据", f"预期>=3个, 实际{len(products)}个")

            # 检查评分维度表
            dimensions_result = await db.execute(select(ScoringDimension))
            dimensions = dimensions_result.scalars().all()

            if len(dimensions) >= 4:
                result.add_pass("TC003: 数据库初始化 - 评分维度")
            else:
                result.add_fail("TC003: 数据库初始化 - 评分维度", f"预期>=4个, 实际{len(dimensions)}个")

    except Exception as e:
        result.add_fail("TC001-003: 数据库初始化", str(e))


async def test_api_data_integrity(result: TestResult):
    """测试2: API数据完整性"""
    try:
        async with AsyncSessionLocal() as db:
            # 检查角色数据完整性
            roles_result = await db.execute(select(CustomerRole))
            role = roles_result.scalars().first()

            if role and role.system_prompt:
                result.add_pass("TC004: 角色数据完整性 - 包含提示词")
            else:
                result.add_fail("TC004: 角色数据完整性", "缺少system_prompt")

            # 检查产品数据完整性
            products_result = await db.execute(select(InsuranceProduct))
            product = products_result.scalars().first()

            if product and product.name and product.description:
                result.add_pass("TC005: 产品数据完整性 - 包含名称和描述")
            else:
                result.add_fail("TC005: 产品数据完整性", "缺少必要字段")

            # 检查评分维度权重总和
            dimensions_result = await db.execute(select(ScoringDimension))
            dimensions = dimensions_result.scalars().all()

            dimension_weights = {}
            for dim in dimensions:
                dimension_weights[dim.name] = dim.weight

            total_weight = sum(dimension_weights.values())
            if abs(total_weight - 100) < 0.1:
                result.add_pass("TC006: 评分维度权重总和为100%")
            else:
                result.add_fail("TC006: 评分维度权重", f"总和为{total_weight}%")

    except Exception as e:
        result.add_fail("TC004-006: API数据完整性", str(e))


async def test_ai_service(result: TestResult):
    """测试3: AI服务配置（模型配置来自 data/model_config.json）"""
    try:
        from app.core import model_store

        # 检查模型配置文件
        models = model_store.load_models()
        if models:
            result.add_pass(f"TC007: 模型配置文件 - {len(models)}个模型")
        else:
            result.add_fail("TC007: 模型配置文件", "无模型配置，请在管理后台添加")

        active_models = [m for m in models if m.get("is_active")]
        if active_models:
            result.add_pass(f"TC008: 启用中的模型 - {len(active_models)}个")
        else:
            result.add_fail("TC008: 启用中的模型", "无启用中的模型")

        # 测试AI服务初始化（按第一个启用模型）
        try:
            ai_service = AIService(
                api_key=active_models[0]["api_key"],
                base_url=active_models[0].get("api_base") or None,
                model=active_models[0]["model_name"],
            )
            result.add_pass("TC009: AI服务初始化")
        except IndexError:
            result.add_fail("TC009: AI服务初始化", "无启用模型可初始化")
        except Exception as e:
            result.add_fail("TC009: AI服务初始化", str(e))

    except Exception as e:
        result.add_fail("TC007-009: AI服务测试", str(e))


async def run_all_tests():
    """运行所有测试"""
    print("[INFO] 开始自动化测试...")
    print(f"{'='*50}\n")

    result = TestResult()

    # 测试数据库
    await test_database_init(result)

    # 测试API数据
    await test_api_data_integrity(result)

    # 测试AI服务
    await test_ai_service(result)

    # 打印总结
    success = result.summary()

    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
