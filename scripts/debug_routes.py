"""
路由诊断脚本 - 检查 /api/models/ 404 问题
"""
import sys
import asyncio
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from main import app
from fastapi.routing import APIRoute

def analyze_routes():
    """分析所有注册的路由"""
    print("=" * 80)
    print("路由诊断报告")
    print("=" * 80)

    # 1. 检查所有路由
    print("\n【1】所有已注册的路由:")
    print("-" * 80)

    models_routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            # 检查路径是否包含 models
            if 'models' in route.path.lower():
                models_routes.append(route)
                print(f"  路径: {route.path}")
                print(f"  方法: {route.methods}")
                print(f"  端点: {route.endpoint}")
                print(f"  标签: {route.tags}")
                print("-" * 80)

    # 2. 统计信息
    print(f"\n【2】统计信息:")
    print(f"  总路由数: {len([r for r in app.routes if isinstance(r, APIRoute)])}")
    print(f"  models 相关路由数: {len(models_routes)}")

    # 3. 检查特定路径
    print("\n【3】检查特定路径是否存在:")
    target_paths = [
        "/api/models",
        "/api/models/",
        "/models",
        "/models/"
    ]

    for target in target_paths:
        found = False
        for route in app.routes:
            if isinstance(route, APIRoute) and route.path == target:
                found = True
                print(f"  ✓ {target} - 存在")
                break
        if not found:
            print(f"  ✗ {target} - 不存在")

    # 4. 检查路由器注册
    print("\n【4】APIRouter 注册信息:")
    print(f"  app.router 路由数: {len(app.routes)}")

    # 5. 详细的路由路径分析
    print("\n【5】所有路由路径列表:")
    for idx, route in enumerate(app.routes):
        if isinstance(route, APIRoute):
            print(f"  {idx + 1}. [{', '.join(route.methods)}] {route.path}")

    # 6. 检查是否有重复路径
    print("\n【6】检查路径重复:")
    path_counts = {}
    for route in app.routes:
        if isinstance(route, APIRoute):
            path = route.path
            if path not in path_counts:
                path_counts[path] = []
            path_counts[path].append(route.methods)

    duplicates = {k: v for k, v in path_counts.items() if len(v) > 1}
    if duplicates:
        print("  发现重复路径:")
        for path, methods in duplicates.items():
            print(f"    {path}: {methods}")
    else:
        print("  ✓ 没有发现重复路径")

    return models_routes

def test_import():
    """测试导入"""
    print("\n【7】测试模块导入:")
    print("-" * 80)

    try:
        from app.api import models
        print("  ✓ app.api.models 导入成功")

        # 检查 router 对象
        if hasattr(models, 'router'):
            print(f"  ✓ models.router 存在")
            print(f"    - prefix: {models.router.prefix}")
            print(f"    - tags: {models.router.tags}")
            print(f"    - 路由数量: {len(models.router.routes)}")

            # 列出所有子路由
            print("\n    models.router 的所有路由:")
            for route in models.router.routes:
                if isinstance(route, APIRoute):
                    print(f"      - [{', '.join(route.methods)}] {route.path}")
        else:
            print("  ✗ models.router 不存在")

    except Exception as e:
        print(f"  ✗ 导入失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        # 分析路由
        models_routes = analyze_routes()

        # 测试导入
        test_import()

        print("\n" + "=" * 80)
        print("诊断完成")
        print("=" * 80)

        if not models_routes:
            print("\n⚠️  警告: 没有找到任何 models 相关的路由!")
            print("这可能意味着路由没有被正确注册。")
        else:
            print(f"\n✓ 找到 {len(models_routes)} 个 models 相关路由")

    except Exception as e:
        print(f"\n❌ 诊断过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
