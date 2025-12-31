# 诊断工具使用指南

## 工具列表

### 1. verify_fix.py - 验证修复
**用途**: 验证 /api/models/ 端点是否正常工作

**使用方法**:
```bash
cd backend
python verify_fix.py
```

**输出**:
- 服务器状态检查
- OpenAPI 文档检查
- 端点功能测试
- 修复结果报告

---

### 2. debug_routes.py - 路由诊断
**用途**: 检查应用中注册的所有路由

**使用方法**:
```bash
cd backend
python debug_routes.py
```

**输出**:
- 所有已注册的路由列表
- models 相关路由详情
- 路由统计信息
- 路径冲突检查

---

### 3. test_endpoint.py - 端点测试
**用途**: 使用 httpx 测试各个 API 端点

**使用方法**:
```bash
cd backend
python test_endpoint.py
```

**测试端点**:
- `/` - 根路径
- `/health` - 健康检查
- `/api/roles/` - Roles API
- `/api/models/` - Models API

---

### 4. check_running_server.py - 服务器状态检查
**用途**: 检查运行中的服务器实际加载的路由

**使用方法**:
```bash
cd backend
python check_running_server.py
```

**输出**:
- 服务器运行状态
- OpenAPI 文档中的路径
- models 路径是否存在
- 端点响应测试

---

### 5. runtime_test.py - TestClient 测试
**用途**: 使用 FastAPI TestClient 在内存中测试路由

**使用方法**:
```bash
cd backend
python runtime_test.py
```

**特点**:
- 不依赖运行中的服务器
- 使用最新代码
- 快速验证路由配置

---

### 6. simple_route_check.py - 简单路由检查
**用途**: 快速列出所有路由,突出显示 models 路由

**使用方法**:
```bash
cd backend
python simple_route_check.py
```

**输出**:
- 所有路由的简洁列表
- models 路由标记
- 统计信息

---

### 7. test_server_start.py - 启动流程测试
**用途**: 测试服务器启动时的模块加载

**使用方法**:
```bash
cd backend
python test_server_start.py
```

**检查项**:
- main 模块导入
- 应用对象创建
- 路由注册
- models 模块导入
- TestClient 验证

---

## 使用场景

### 场景 1: 端点返回 404
1. 运行 `check_running_server.py` 检查服务器状态
2. 运行 `runtime_test.py` 确认代码正确性
3. 如果代码正确但服务器缺少路由 → 重启服务器
4. 运行 `verify_fix.py` 验证修复

### 场景 2: 添加新路由后验证
1. 运行 `debug_routes.py` 确认路由已注册
2. 运行 `runtime_test.py` 测试路由功能
3. 重启服务器
4. 运行 `verify_fix.py` 验证

### 场景 3: 日常开发
1. 修改代码后等待自动重载
2. 运行 `test_endpoint.py` 快速测试
3. 或运行 `verify_fix.py` 完整验证

### 场景 4: 诊断疑难问题
1. `simple_route_check.py` - 快速查看路由
2. `debug_routes.py` - 详细路由信息
3. `check_running_server.py` - 服务器实际状态
4. `runtime_test.py` - 代码层面验证
5. `test_server_start.py` - 启动流程检查

---

## 工具对比

| 工具 | 是否需要服务器运行 | 测试内容 | 适用场景 |
|------|-------------------|----------|----------|
| verify_fix.py | ✅ 需要 | 完整验证 | 修复后验证 |
| debug_routes.py | ❌ 不需要 | 路由注册 | 代码检查 |
| test_endpoint.py | ✅ 需要 | 端点响应 | 功能测试 |
| check_running_server.py | ✅ 需要 | 服务器状态 | 诊断问题 |
| runtime_test.py | ❌ 不需要 | TestClient | 代码验证 |
| simple_route_check.py | ❌ 不需要 | 路由列表 | 快速查看 |
| test_server_start.py | ❌ 不需要 | 启动流程 | 启动问题 |

---

## 输出编码说明

部分工具可能遇到 Windows 控制台编码问题(gbk vs utf-8)。

**解决方案**:
1. 使用 PowerShell 运行(编码支持更好)
2. 只关注关键的数字和路径信息
3. 使用 `runtime_test.py` 或 `verify_fix.py`(编码友好)

---

## 常见诊断流程

### 流程 A: 端点 404 问题
```
verify_fix.py
  ↓ 失败
check_running_server.py
  ↓ OpenAPI 中没有路径
runtime_test.py
  ↓ 成功(代码正确)
结论: 服务器使用旧代码
解决: 重启服务器
```

### 流程 B: 新路由不工作
```
debug_routes.py
  ↓ 路由已注册
runtime_test.py
  ↓ TestClient 成功
重启服务器
verify_fix.py
  ↓ 成功
解决: 完成
```

### 流程 C: 完整诊断
```
1. simple_route_check.py - 快速查看
2. debug_routes.py - 详细信息
3. runtime_test.py - 代码测试
4. check_running_server.py - 服务器测试
5. verify_fix.py - 最终验证
```

---

## 维护说明

### 添加新诊断工具
1. 在 `backend/` 目录创建新的 Python 脚本
2. 使用清晰的命名: `[功能]_test.py` 或 `check_[对象].py`
3. 添加详细的使用说明
4. 更新本索引文件

### 修改现有工具
1. 保持输出格式一致
2. 添加错误处理
3. 支持编码问题
4. 更新文档

---

## 总结

这些工具帮助快速诊断和解决 API 端点问题:

- **验证修复**: `verify_fix.py`
- **检查代码**: `runtime_test.py`, `debug_routes.py`
- **检查服务器**: `check_running_server.py`, `test_endpoint.py`
- **快速查看**: `simple_route_check.py`

记住: **代码正确 ≠ 服务器使用新代码**

修改代码后,确保:
1. 等待自动重载,或
2. 手动重启服务器

然后使用 `verify_fix.py` 验证!
