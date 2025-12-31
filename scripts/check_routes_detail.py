"""
详细路由检查 - 检查路由顺序和优先级
"""
from main import app
from fastapi.routing import APIRoute, APIRouter
from fastapi import FastAPI

def check_route_details():
    """检查路由详细信息"""
    print("=" * 80)
    print("FastAPI 路由详细信息")
    print("=" * 80)

    # 按顺序检查所有路由
    print("\n【路由注册顺序】")
    for idx, route in enumerate(app.routes):
        if isinstance(route, APIRoute):
            print(f"\n{idx + 1}. 路径: {route.path}")
            print(f"   方法: {route.methods}")
            print(f"   端点函数: {route.endpoint.__name__}")
            print(f"   所属模块: {route.endpoint.__module__}")

            # 检查路由依赖
            if route.endpoint.__dependencies__:
                print(f"   依赖项: {route.endpoint.__dependencies__}")

    # 检查是否有路径冲突
    print("\n\n【路径冲突检查】")
    path_map = {}
    for route in app.routes:
        if isinstance(route, APIRoute):
            if route.path not in path_map:
                path_map[route.path] = []
            path_map[route.path].extend(route.methods)

    for path, methods in sorted(path_map.items()):
        if 'models' in path.lower():
            print(f"\n路径: {path}")
            print(f"  方法: {set(methods)}")

    # 检查路由器对象
    print("\n\n【APIRouter 对象检查】")
    print(f"应用类型: {type(app)}")
    print(f"总路由数: {len(app.routes)}")

    # 检查每个路由器的路由
    router_routes = [r for r in app.routes if isinstance(r, APIRouter)]
    print(f"APIRouter 数量: {len(router_routes)}")

    # 检查所有 models 相关路由
    print("\n\n【Models 相关路由详情】")
    models_count = 0
    for route in app.routes:
        if isinstance(route, APIRoute) and 'models' in route.path.lower():
            models_count += 1
            print(f"\n{models_count}. {route.path}")
            print(f"   方法: {route.methods}")
            print(f"   函数: {route.endpoint.__name__}")

    print(f"\n共找到 {models_count} 个 models 相关路由")

    # 检查应用状态
    print("\n\n【应用状态】")
    print(f"应用已启动: {hasattr(app, 'router')}")
    print(f"Router 类型: {type(app.router)}")
    print(f"Router 中的路由数: {len(app.router.routes)}")

if __name__ == "__main__":
    try:
        check_route_details()
        print("\n" + "=" * 80)
        print("检查完成")
        print("=" * 80)
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()
