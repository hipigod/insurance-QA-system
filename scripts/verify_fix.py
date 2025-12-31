"""
验证修复 - 检查 /api/models/ 端点是否正常工作
"""
import httpx
import asyncio
import sys

def print_success(msg):
    print(f"[OK] {msg}")

def print_error(msg):
    print(f"[ERROR] {msg}")

def print_info(msg):
    print(f"[INFO] {msg}")

async def verify_fix():
    """验证修复是否成功"""
    print("=" * 70)
    print("验证 /api/models/ 端点修复")
    print("=" * 70)

    base_url = "http://127.0.0.1:8000"

    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. 检查服务器是否运行
        print("\n[步骤 1] 检查服务器状态...")
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print_success("服务器正在运行")
            else:
                print_error(f"服务器状态异常: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"无法连接到服务器: {e}")
            print_info("请确保后端服务正在运行")
            print_info("运行命令: cd backend && python main.py")
            return False

        # 2. 检查 OpenAPI 文档
        print("\n[步骤 2] 检查 OpenAPI 文档...")
        try:
            response = await client.get(f"{base_url}/openapi.json")
            if response.status_code == 200:
                openapi = response.json()
                paths = openapi.get('paths', {})

                models_paths = [p for p in paths if 'models' in p.lower()]

                if models_paths:
                    print_success(f"找到 {len(models_paths)} 个 models 相关路径")

                    print("\n  Models API 端点:")
                    for path in sorted(models_paths):
                        methods = list(paths[path].keys())
                        print(f"    {path}: {', '.join(methods)}")
                else:
                    print_error("OpenAPI 文档中没有 models 路径")
                    print_info("这说明服务器仍在使用旧代码")
                    print_info("解决方案: 重启后端服务器")
                    return False
            else:
                print_error(f"获取 OpenAPI 文档失败: {response.status_code}")
                return False
        except Exception as e:
            print_error(f"检查 OpenAPI 文档异常: {e}")
            return False

        # 3. 测试 /api/models/ 端点
        print("\n[步骤 3] 测试 /api/models/ 端点...")
        try:
            response = await client.get(f"{base_url}/api/models/")
            if response.status_code == 200:
                print_success("/api/models/ 端点正常工作")
                data = response.json()
                print_info(f"返回 {len(data)} 条模型配置数据")
                return True
            else:
                print_error(f"/api/models/ 返回错误: {response.status_code}")
                print_info(f"详情: {response.json()}")
                return False
        except Exception as e:
            print_error(f"请求失败: {e}")
            return False

    print("=" * 70)

if __name__ == "__main__":
    result = asyncio.run(verify_fix())

    print("\n" + "=" * 70)
    if result:
        print("验证成功!")
        print("\n问题已解决,/api/models/ 端点现在可以正常访问。")
        print("\n可以访问以下地址:")
        print("  - API 文档: http://127.0.0.1:8000/docs")
        print("  - Models API: http://127.0.0.1:8000/api/models/")
    else:
        print("验证失败!")
        print("\n可能的原因:")
        print("  1. 后端服务器仍在使用旧代码")
        print("  2. 解决方案: 重启后端服务器")
        print("\n重启方法:")
        print("  方式 1: 运行 restart_backend.bat")
        print("  方式 2: 手动停止后端服务窗口,然后运行: cd backend && python main.py")
    print("=" * 70)

    sys.exit(0 if result else 1)
