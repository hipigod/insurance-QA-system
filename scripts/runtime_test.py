"""
运行时路由测试 - 使用 TestClient
"""
from fastapi.testclient import TestClient
from main import app

def test_routes():
    """使用 TestClient 测试路由"""
    print("=" * 80)
    print("使用 TestClient 测试路由")
    print("=" * 80)

    client = TestClient(app)

    test_cases = [
        ("根路径", "/", "GET"),
        ("健康检查", "/health", "GET"),
        ("Roles API", "/api/roles/", "GET"),
        ("Models API", "/api/models/", "GET"),
    ]

    for name, path, method in test_cases:
        print(f"\n测试: {name}")
        print(f"路径: {path}")

        try:
            if method == "GET":
                response = client.get(path)

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                print(f"成功: {response.json()[:100] if len(str(response.json())) > 100 else response.json()}")
            elif response.status_code == 404:
                print(f"错误: 404 Not Found")
                print(f"详情: {response.json()}")
            else:
                print(f"响应: {response.text[:200]}")

        except Exception as e:
            print(f"异常: {e}")

    print("\n" + "=" * 80)

    # 检查所有路由
    print("\n应用中的所有路由:")
    for route in app.routes:
        if hasattr(route, 'path') and 'models' in route.path.lower():
            print(f"  {route.path}")

if __name__ == "__main__":
    test_routes()
