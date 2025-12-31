"""
直接测试 API 端点
"""
import httpx
import asyncio

async def test_endpoints():
    """测试各个端点"""
    base_url = "http://127.0.0.1:8000"

    print("=" * 60)
    print("API 端点测试")
    print("=" * 60)

    test_cases = [
        ("根路径", "/"),
        ("健康检查", "/health"),
        ("Roles API", "/api/roles/"),
        ("Models API", "/api/models/"),
        ("Models API (无斜杠)", "/api/models"),
    ]

    async with httpx.AsyncClient() as client:
        for name, path in test_cases:
            url = f"{base_url}{path}"
            print(f"\n测试: {name}")
            print(f"URL: {url}")

            try:
                response = await client.get(url, timeout=5.0)
                print(f"状态码: {response.status_code}")

                if response.status_code == 200:
                    print(f"响应: {response.json()}")
                elif response.status_code == 404:
                    print("错误: 404 Not Found")
                    print(f"响应内容: {response.text[:200]}")
                else:
                    print(f"响应: {response.text[:200]}")

            except httpx.ConnectError:
                print("错误: 无法连接到服务器")
                print("请确保后端服务正在运行")
            except Exception as e:
                print(f"错误: {e}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(test_endpoints())
