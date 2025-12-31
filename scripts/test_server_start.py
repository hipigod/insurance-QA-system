"""
测试服务器启动和路由加载
"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

def test_startup():
    """测试启动时的路由加载"""
    print("=" * 80)
    print("测试服务器启动")
    print("=" * 80)

    print("\n【步骤 1】导入 main 模块...")
    try:
        from main import app
        print("✓ main 模块导入成功")
    except Exception as e:
        print(f"✗ main 模块导入失败: {e}")
        import traceback
        traceback.print_exc()
        return

    print("\n【步骤 2】检查应用对象...")
    print(f"  应用类型: {type(app)}")
    print(f"  应用标题: {app.title}")

    print("\n【步骤 3】检查所有路由...")
    from fastapi.routing import APIRoute

    models_routes = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            if 'models' in route.path.lower():
                models_routes.append(route)

    print(f"  总路由数: {len([r for r in app.routes if isinstance(r, APIRoute)])}")
    print(f"  models 路由数: {len(models_routes)}")

    if models_routes:
        print("\n  Models 路由列表:")
        for route in models_routes:
            print(f"    - [{', '.join(route.methods)}] {route.path}")
    else:
        print("\n  ⚠️  警告: 没有找到 models 路由!")

    print("\n【步骤 4】检查导入的 models 模块...")
    try:
        from app.api import models as models_module
        print(f"  ✓ models 模块已导入")
        print(f"  - Router prefix: {models_module.router.prefix}")
        print(f"  - Router routes: {len(models_module.router.routes)}")
    except Exception as e:
        print(f"  ✗ models 模块导入失败: {e}")

    print("\n【步骤 5】检查 main.py 中的导入语句...")
    try:
        with open('main.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'from app.api import' in content:
                print("  ✓ 发现导入语句")
                # 提取导入行
                for line in content.split('\n'):
                    if 'from app.api import' in line:
                        print(f"    {line.strip()}")

                        # 检查是否包含 models
                        if 'models' in line:
                            print(f"      ✓ models 在导入列表中")
                        else:
                            print(f"      ✗ models 不在导入列表中")
            else:
                print("  ✗ 没有找到导入语句")
    except Exception as e:
        print(f"  ✗ 读取文件失败: {e}")

    print("\n" + "=" * 80)
    print("诊断完成")
    print("=" * 80)

    # 检查路由是否真的包含在应用中
    print("\n【最终验证】")
    from fastapi.testclient import TestClient
    client = TestClient(app)

    try:
        response = client.get("/api/models/")
        print(f"  TestClient 测试 /api/models/: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✓ TestClient 测试成功!")
        else:
            print(f"  ✗ TestClient 测试失败: {response.json()}")
    except Exception as e:
        print(f"  ✗ TestClient 测试异常: {e}")

if __name__ == "__main__":
    test_startup()
