"""
系统功能快速测试
"""
import requests
import time

print("=" * 60)
print("保险销售智能陪练系统 - 功能测试")
print("=" * 60)

# 等待后端完全启动
print("\n等待后端服务启动...")
for i in range(10):
    try:
        response = requests.get("http://127.0.0.1:8000/health", timeout=2)
        if response.status_code == 200:
            print("[OK] 后端服务运行正常")
            break
    except:
        time.sleep(1)
        print(f"   等待中... ({i+1}/10)")
else:
    print("[ERROR] 后端服务启动失败!")
    exit(1)

# 测试各个API端点
tests = [
    ("角色列表", "http://127.0.0.1:8000/api/roles/"),
    ("产品列表", "http://127.0.0.1:8000/api/products/"),
    ("维度列表", "http://127.0.0.1:8000/api/dimensions/"),
    ("案例列表", "http://127.0.0.1:8000/api/cases/"),
    ("模型配置", "http://127.0.0.1:8000/api/models/"),
]

print("\n测试API端点:")
for name, url in tests:
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            count = len(data) if isinstance(data, list) else 1
            print(f"  [OK] {name}: {count}条记录")
        else:
            print(f"  [WARN] {name}: HTTP {response.status_code}")
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")

# 显示访问地址
print("\n" + "=" * 60)
print("系统访问地址:")
print("=" * 60)
print("前端应用: http://localhost:5173")
print("API文档:  http://127.0.0.1:8000/docs")
print("管理后台: http://localhost:5173/#/admin")
print("\n系统已就绪,可以开始使用!")
print("=" * 60)
