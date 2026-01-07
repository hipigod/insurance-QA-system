# 保险销售智能陪练系统 V0.2.2

> AI驱动的保险销售能力提升平台

## 项目简介

本项目是一个面向保险销售人员的AI智能陪练系统，通过模拟真实客户对话场景，帮助销售人员提升沟通能力、产品知识和营销技巧，并提供AI驱动的多维度能力评估。

> 📚 **文档中心**: 查看完整文档请访问 [docs/README.md](docs/README.md)

### 核心功能

- 🤖 **AI对话练习**：智能模拟5种真实客户类型，提供接近真实的沟通体验
- 📊 **多维度评分**：从沟通能力、有效营销、产品熟练度、异议处理4个维度评估
- 🎯 **异议识别**：自动识别价格、信任、需求、竞品等异议类型
- 💡 **优秀案例对比**：针对薄弱环节推送标准话术参考
- ⚙️ **管理后台**：完整的角色、产品、评分维度、案例管理系统
- 🐳 **Docker支持**：一键部署，开箱即用，环境隔离
- 📦 **预设数据**：内置完整的演示数据，无需手动配置

### 技术栈

**后端**：
- FastAPI - 现代异步Web框架
- SQLite - 轻量级数据库
- WebSocket - 实时双向通信
- OpenAI SDK - 兼容国产大模型API

**前端**：
- Vue 3 - 渐进式前端框架
- Vite - 快速构建工具
- Element Plus - UI组件库
- Pinia - 状态管理

**部署**：
- Docker - 容器化部署
- Docker Compose - 多容器编排
- Nginx - 反向代理和静态文件服务

---

## 快速开始

### 部署方式选择

本项目支持两种部署方式：

#### 🐳 方式一：Docker 部署（推荐）

**优点**：一键部署、环境隔离、跨平台、开箱即用

**环境要求**：
- Docker Desktop 已安装并运行
- 国产大模型 API Key（推荐 DeepSeek）

**快速启动**：
```bash
# 1. 克隆项目
git clone https://github.com/hipigod/insurance-QA-system.git
cd insurance-QA-system

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的 MODEL_API_KEY

# 3. 一键启动
docker compose up -d

# 4. 初始化预设数据（首次运行）
docker exec insurance-backend python init_demo_data.py
```

**访问地址**：
- 前端：http://localhost
- 后端 API：http://localhost:8000/docs

**常用命令**：
```bash
# 查看容器状态
docker ps

# 查看日志
docker logs insurance-backend
docker logs insurance-frontend

# 停止服务
docker compose down

# 重启服务
docker compose restart
```

#### 💻 方式二：本地开发模式

**优点**：便于调试、修改代码实时生效

**环境要求**：

- Python 3.9+
- Node.js 16+
- 国产大模型API Key（推荐DeepSeek）

**安装步骤**

#### 1. 克隆项目

```bash
git clone <your-repo-url>
cd Insurance Q&A System
```

#### 2. 后端设置

```bash
# 进入后端目录
cd backend

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入您的 API_KEY
```

#### 3. 前端设置

```bash
# 打开新终端，进入前端目录
cd frontend

# 安装依赖
npm install
```

#### 4. 初始化数据库

```bash
# 在后端目录执行
cd backend
python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

#### 5. 启动项目

**启动后端**（在backend目录）：
```bash
python main.py
```

后端将运行在：http://127.0.0.1:8000

**启动前端**（在frontend目录）：
```bash
npm run dev
```

前端将运行在：http://localhost:5173

---

## 目录结构

```
Insurance Q&A System/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务服务
│   │   └── utils/          # 工具函数
│   ├── data/               # 数据库文件（自动生成）
│   ├── main.py             # 应用入口
│   ├── Dockerfile          # Docker镜像构建
│   └── requirements.txt    # Python依赖
│
├── frontend/               # 前端代码
│   ├── src/
│   │   ├── api/           # API接口
│   │   ├── components/    # 公共组件
│   │   ├── router/        # 路由配置
│   │   ├── stores/        # 状态管理
│   │   ├── utils/         # 工具函数
│   │   ├── views/         # 页面视图
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── package.json       # 依赖配置
│   ├── vite.config.js     # Vite配置
│   ├── Dockerfile         # Docker镜像构建
│   └── nginx.conf         # Nginx配置
│
├── scripts/               # 工具脚本
│   └── init_demo_data.py  # 数据初始化脚本
│
├── docs/                   # 文档目录
├── docker-compose.yml      # Docker编排配置
├── .env.example            # 环境变量模板
├── .gitignore              # Git忽略文件
└── README.md               # 项目说明
```

---

## 配置说明

### 后端配置（.env）

```env
# AI模型配置 - DeepSeek(推荐)
DEFAULT_MODEL=deepseek-chat
MODEL_API_KEY=your_deepseek_api_key_here
MODEL_API_BASE=https://api.deepseek.com/v1

# 如果使用通义千问,取消下面的注释并注释掉上面的配置
# DEFAULT_MODEL=qwen-plus
# MODEL_API_KEY=your_qwen_api_key_here
# MODEL_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1

# 对话配置
AI_RESPONSE_TIMEOUT=25  # AI响应超时时间(秒)
AI_TEMPERATURE=0.7      # AI创意度(0-1)
```

**重要提示**：
1. 首次使用需要配置有效的API Key
2. 推荐使用DeepSeek（免费额度大、响应快）
3. 修改.env后需要重启后端服务才能生效

### 前端配置

前端代理配置已设置在 `vite.config.js`，默认代理后端的 `/api` 和 `/ws` 路径。

---

## 使用指南

### 1. 选择场景

- 从角色列表选择一个客户角色（小白客户、懂行客户、难缠客户等）
- 从产品列表选择一个保险产品

### 2. 开始对话

- AI客户会主动打招呼
- 输入您的回复进行对话练习
- 可随时结束对话

### 3. 查看评分

- 结束对话后系统会自动评分
- 查看各维度得分和评价
- 学习优秀案例对比

### 4. 历史记录

- 系统会自动保存最近10次练习记录
- 可随时查看历史练习详情

---

## API文档

启动后端后，访问：http://127.0.0.1:8000/docs

---

## 常见问题

### Q: Docker部署后如何初始化预设数据？

A: 首次启动Docker容器后，运行以下命令初始化预设数据：
```bash
docker exec insurance-backend python init_demo_data.py
```

这会自动创建：
- 5个客户角色（小白客户、懂行客户、难缠客户、犹豫客户等）
- 3个保险产品（重疾险、医疗险、寿险）
- 4个评分维度（沟通能力、有效营销、产品熟练度、异议处理）

### Q: 如何获取AI模型的API Key？

A: 本项目推荐使用DeepSeek，访问 https://platform.deepseek.com/ 注册并获取API Key。

### Q: 支持哪些国产大模型？

A: 支持所有兼容OpenAI API格式的国产大模型，如：
- **DeepSeek**（推荐） - 响应快、免费额度大
- 智谱AI (ChatGLM)
- 百度文心一言
- 阿里通义千问
- 月之暗面 (Kimi)
- 等等

配置方法：编辑 `backend/.env` 文件中的相关配置

### Q: 数据存储在哪里？

A: **Docker部署模式**：
- 使用Docker命名卷 `backend-data` 持久化数据库
- 数据存储路径：`/app/data/insurance_practice.db` (容器内)
- 对话记录：浏览器LocalStorage（前端）

**本地开发模式**：
- 所有数据都存储在本地
- 对话记录：浏览器LocalStorage（前端）
- 角色配置：SQLite数据库（后端data目录）
- 产品信息：SQLite数据库（后端data目录）
- 评分记录：浏览器LocalStorage（前端）

**注意**：清除浏览器数据会导致对话记录丢失，请注意备份。

### Q: Docker容器数据会丢失吗？

A: 不会。本项目使用Docker命名卷（`backend-data`）来持久化数据库数据。即使容器被删除，数据也会保留。如需完全清理数据：
```bash
# 停止并删除容器和卷
docker compose down -v
```

### Q: 如何自定义角色和产品？

A: 通过管理后台界面：
1. 点击首页右上角"管理后台"按钮
2. 在相应标签页进行增删改查操作
3. 支持自定义角色、产品、评分维度、优秀案例

---

## 版本历史

### V0.2.2 (2026-01-07)
- 🐳 **Docker部署优化**：修复Docker容器数据库初始化问题
- ✅ **一键部署**：添加完整的Docker Compose配置
- 📦 **预设数据**：提供数据初始化脚本，包含5个角色、3个产品、4个评分维度
- 🔧 **配置优化**：简化数据库连接配置，提升容器稳定性
- 📝 **文档更新**：添加Docker部署文档和快速启动指南

### V0.2.1 (2025-12-31)
- 🐛 **修复评分跳转Bug**: 修复对话结束后无法跳转到结果页面的问题
- ⚡ **优化超时配置**: 评分超时从15秒增加到30秒,确保复杂对话能正常评分
- 🔍 **添加调试日志**: 完整的评分流程日志,便于问题排查
- ✅ **测试验证**: 通过多轮测试验证AI对话、评分、跳转全流程正常
- 📝 **改进错误处理**: 更友好的错误提示和异常处理机制

### V0.2.0 (2025-12-31)
- ✅ **新增管理后台**：完整的角色、产品、评分维度、案例管理功能
- ✅ **优化超时配置**：前端30秒/后端25秒,避免AI响应超时
- ✅ **修复数据加载**：修复管理后台数据不显示问题
- ✅ **改进错误处理**：更友好的错误提示和异常处理
- ✅ **性能优化**：AI连接测试通过,响应速度<5秒
- ✅ **配置优化**：支持多种国产大模型配置切换

### V1.2.0 (2025-12-30)
- ✅ 实现WebSocket实时对话
- ✅ 实现多维度AI评分
- ✅ 实现异议类型识别
- ✅ 实现优秀案例对比
- ✅ 移动端适配优化

### 计划功能
- ⏳ 产品文档自动解析
- ⏳ 语音对话功能
- ⏳ 数据导出功能
- ⏳ 用户系统

---

## 贡献指南

欢迎提交Issue和Pull Request！

---

## 许可证

MIT License

---

## 联系方式

如有问题，请提交Issue或联系项目维护者。

---

**🚀 立即开始，提升您的保险销售能力！**
