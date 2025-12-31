"""
检查运行中的代码版本
"""
import inspect
from main import app
from app.api import models

print("=" * 80)
print("检查运行中的代码版本")
print("=" * 80)

# 检查 models 模块的路由定义
print("\n【1】Models 模块信息:")
print(f"  模块文件: {models.__file__}")
print(f"  Router 对象: {models.router}")
print(f"  Router prefix: {models.router.prefix}")

# 检查 main.py 中的导入
print("\n【2】Main.py 导入信息:")
main_file = inspect.getfile(app)
print(f"  Main 文件: {main_file}")

# 读取 main.py 内容
with open(main_file, 'r', encoding='utf-8') as f:
    main_content = f.read()

# 检查 models 导入
print("\n【3】Main.py 中的 models 导入:")
for line_num, line in enumerate(main_content.split('\n'), 1):
    if 'from app.api import' in line:
        print(f"  第 {line_num} 行: {line.strip()}")
        if 'models' in line:
            print(f"    >>> 包含 models")

# 检查路由注册
print("\n【4】路由注册:")
for line_num, line in enumerate(main_content.split('\n'), 1):
    if 'include_router' in line and 'models' in line:
        print(f"  第 {line_num} 行: {line.strip()}")

# 检查路由是否在应用中
print("\n【5】应用中的路由:")
from fastapi.routing import APIRoute
models_in_app = [r for r in app.routes if isinstance(r, APIRoute) and 'models' in r.path.lower()]
print(f"  找到 {len(models_in_app)} 个 models 路由")

if len(models_in_app) > 0:
    print("\n  路由列表:")
    for route in models_in_app:
        print(f"    - {route.path}")

# 检查文件修改时间
import os
import datetime

print("\n【6】文件修改时间:")
files_to_check = [
    'backend/main.py',
    'backend/app/api/models.py',
]

for file_path in files_to_check:
    full_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), file_path)
    if os.path.exists(full_path):
        mtime = os.path.getmtime(full_path)
        mtime_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"  {file_path}: {mtime_str}")

print("\n" + "=" * 80)
