"""
简单路由检查
"""
from main import app
from fastapi.routing import APIRoute

def simple_check():
    """简单检查所有路由"""
    print("=" * 80)
    print("所有已注册的路由")
    print("=" * 80)

    models_routes = []

    for idx, route in enumerate(app.routes):
        if isinstance(route, APIRoute):
            path_info = f"{idx + 1}. [{', '.join(route.methods)}] {route.path}"

            if 'models' in route.path.lower():
                models_routes.append(route)
                path_info += " <-- MODELS"

            print(path_info)

    print("\n" + "=" * 80)
    print(f"总计: {len([r for r in app.routes if isinstance(r, APIRoute)])} 个路由")
    print(f"Models 相关: {len(models_routes)} 个路由")
    print("=" * 80)

    if models_routes:
        print("\nModels 路由详情:")
        for route in models_routes:
            print(f"  - {route.path}")
            print(f"    方法: {route.methods}")
            print(f"    函数: {route.endpoint.__name__}")
            print(f"    模块: {route.endpoint.__module__}")

if __name__ == "__main__":
    simple_check()
