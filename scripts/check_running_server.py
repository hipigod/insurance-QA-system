"""
检查运行中的服务器状态
"""
import httpx
import asyncio

async def check_server():
    """检查服务器状态"""
    base_url = "http://127.0.0.1:8000"

    print("=" * 80)
    print("检查运行中的服务器")
    print("=" * 80)

    async with httpx.AsyncClient(timeout=5.0) as client:
        # 1. 检查服务器是否运行
        print("\n【1】检查服务器状态...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"  服务器状态: {response.status_code}")
        except Exception as e:
            print(f"  服务器未运行或无法连接: {e}")
            return

        # 2. 获取 OpenAPI 文档
        print("\n【2】检查 OpenAPI 文档...")
        try:
            response = await client.get(f"{base_url}/openapi.json")
            if response.status_code == 200:
                openapi = response.json()
                paths = openapi.get('paths', {})

                print(f"  OpenAPI 文档中的路径数量: {len(paths)}")

                # 检查是否有 models 路径
                models_paths = [p for p in paths if 'models' in p.lower()]
                print(f"  Models 相关路径数量: {len(models_paths)}")

                if models_paths:
                    print("\n  Models 路径列表:")
                    for path in sorted(models_paths):
                        methods = list(paths[path].keys())
                        print(f"    {path}: {methods}")
                else:
                    print("\n  ⚠️  警告: OpenAPI 文档中没有 models 路径!")
                    print("\n  所有路径:")
                    for path in sorted(paths.keys()):
                        print(f"    - {path}")

            else:
                print(f"  获取 OpenAPI 文档失败: {response.status_code}")

        except Exception as e:
            print(f"  获取 OpenAPI 文档异常: {e}")

        # 3. 直接测试 /api/models/
        print("\n【3】直接测试 /api/models/ 端点...")
        try:
            response = await client.get(f"{base_url}/api/models/")
            print(f"  状态码: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✓ 端点正常工作!")
                data = response.json()
                print(f"  返回数据: {data}")
            else:
                print(f"  ✗ 端点返回错误: {response.json()}")
        except Exception as e:
            print(f"  ✗ 请求失败: {e}")

        # 4. 对比其他端点
        print("\n【4】对比其他端点...")
        test_endpoints = [
            "/api/roles/",
            "/api/products/",
        ]

        for endpoint in test_endpoints:
            try:
                response = await client.get(f"{base_url}{endpoint}")
                status = "✓" if response.status_code == 200 else "✗"
                print(f"  {status} {endpoint}: {response.status_code}")
            except Exception as e:
                print(f"  ✗ {endpoint}: {e}")

    print("\n" + "=" * 80)
    print("诊断完成")
    print("=" * 80)

    print("\n【结论】")
    print("如果 OpenAPI 文档中没有 /api/models/ 路径,")
    print("说明运行中的服务器使用的是旧版本代码,需要重启。")

if __name__ == "__main__":
    asyncio.run(check_server())
