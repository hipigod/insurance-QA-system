# 🚀 系统部署和运行完整指南

## ✅ 当前状态

- ✅ **前端依赖已安装完成** (149个包)
- ⏳ **后端依赖正在安装** (pydantic-core构建中，需要几分钟)
- ⏳ **待执行**: 初始化数据库、启动服务

---

## 📋 部署步骤

### 步骤1: 确认后端依赖安装完成

**检查后端安装状态**:
```bash
# 打开新终端，运行
cd "e:\codeproject\Insurance Q&A System\backend"
python -c "import fastapi; print('FastAPI已安装')"
```

如果输出"FastAPI已安装"，说明依赖安装成功。

**如果安装时间过长（超过5分钟），可以尝试**:
```bash
# 终止当前安装(Ctrl+C)
# 使用预编译的pydantic-core
python -m pip install pydantic-core --prefer-binary
python -m pip install -r requirements.txt --prefer-binary
```

---

### 步骤2: 初始化演示数据

依赖安装完成后，执行:

```bash
cd "e:\codeproject\Insurance Q&A System"
python init_demo_data.py
```

**预期输出**:
```
==================================================
保险销售智能陪练系统 - 数据初始化脚本
==================================================

🔄 正在初始化数据库...
📝 创建客户角色...
   ✅ 创建了 4 个客户角色
📝 创建保险产品...
   ✅ 创建了 3 个保险产品
📝 创建评分维度...
   ✅ 创建了 4 个评分维度

🎉 演示数据初始化完成！
   - 客户角色: 4 个
   - 保险产品: 3 个
   - 评分维度: 4 个

✅ 现在可以启动系统了！
```

---

### 步骤3: 启动后端服务

**打开终端1** (保持运行，不要关闭):

```bash
cd "e:\codeproject\Insurance Q&A System\backend"
python main.py
```

**预期输出**:
```
🚀 保险销售智能陪练系统 v1.2.0 启动成功！
📍 API地址: http://127.0.0.1:8000/docs
INFO:     Started server process ...
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**如果出现错误**:
- "ModuleNotFoundError": 需要等待依赖安装完成
- "API Key未配置": 检查 .env 文件是否存在
- "端口被占用": 修改 .env 中的 PORT 值

---

### 步骤4: 启动前端服务

**打开终端2** (保持运行，不要关闭):

```bash
cd "e:\codeproject\Insurance Q&A System\frontend"
npm run dev
```

**预期输出**:
```
  VITE v5.0.11  ready in 2345 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

**如果出现错误**:
- "command not found": 需要先安装Node.js
- "依赖缺失": 运行 `npm install`
- "端口被占用": Vite会自动选择其他端口

---

### 步骤5: 访问系统

1. **打开浏览器**
2. **访问**: http://localhost:5173
3. **开始使用**！

---

## 🧪 快速功能验证

### 验证1: 查看角色和产品

1. 首页应该显示4个客户角色
2. 首页应该显示3个保险产品
3. 点击"开始对话练习"按钮应该可用

### 验证2: 测试AI对话

1. 选择任意角色和产品
2. 点击"开始对话练习"
3. 观察是否收到AI首次问候（可能需要几秒）

### 验证3: 测试管理后台

1. 返回首页
2. 点击"管理后台"链接
3. 尝试编辑一个角色
4. 查看数据导出功能

---

## ⚠️ 常见问题解决

### 问题1: 依赖安装卡住

**原因**: pydantic-core需要从源码编译，可能需要2-5分钟

**解决**:
- 耐心等待
- 或使用 `--prefer-binary` 选项
- 或使用国内预编译包

### 问题2: AI调用失败

**原因**: API Key配置错误或网络问题

**解决**:
1. 检查 .env 文件是否在 backend 目录下
2. 确认API Key格式: `sk-8b1831a371984c6483b413a759463619`
3. 测试网络连接

### 问题3: 前端无法连接后端

**原因**: 后端未启动或端口错误

**解决**:
1. 确认后端终端显示"启动成功"
2. 访问 http://127.0.0.1:8000/docs 查看API文档
3. 检查前端代理配置

### 问题4: WebSocket连接失败

**原因**: 端口不匹配

**解决**:
1. 确认后端运行在8000端口
2. 打开浏览器控制台查看错误信息
3. 检查WebSocket URL

---

## 📊 系统运行检查清单

启动成功后，请确认以下各项:

- [ ] 后端终端显示"启动成功"
- [ ] 前端终端显示"ready in ... ms"
- [ ] 浏览器可以访问 http://localhost:5173
- [ ] 首页显示角色和产品列表
- [ ] API文档可以访问: http://127.0.0.1:8000/docs
- [ ] .env文件包含正确的API Key
- [ ] 数据库文件已生成 (backend/data/insurance_practice.db)

---

## 🎯 下一步

系统启动成功后，您可以:

1. **体验AI对话**: 选择角色和产品开始练习
2. **配置数据**: 在管理后台编辑角色和产品
3. **查看评分**: 完成对话后查看AI评分报告
4. **导出数据**: 在管理后台导出练习记录

---

## 📞 需要帮助?

如果遇到问题:

1. **查看日志**: 检查后端和前端终端的错误信息
2. **查看文档**: README.md, QUICKSTART.md, DEPLOYMENT.md
3. **查看测试**: TEST_PLAN.md, TEST_REPORT.md
4. **询问我**: 随时告诉我具体问题

---

## 💾 重要提示

- **不要关闭终端窗口** - 服务运行时必须保持终端开启
- **API Key安全** - .env文件不要提交到Git
- **数据备份** - 定期导出练习记录
- **浏览器推荐** - Chrome/Edge/Firefox最新版本

---

**祝您使用愉快！** 🎊
