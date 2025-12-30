# 保险销售智能陪练系统 Demo V1.2

> AI驱动的保险销售能力提升平台

## 项目简介

本项目是一个面向保险销售人员的AI智能陪练系统，通过模拟真实客户对话场景，帮助销售人员提升沟通能力、产品知识和营销技巧，并提供AI驱动的多维度能力评估。

### 核心功能

- 🤖 **AI对话练习**：智能模拟多种真实客户类型，提供接近真实的沟通体验
- 📊 **多维度评分**：从沟通能力、有效营销、产品熟练度、异议处理4个维度评估
- 🎯 **异议识别**：自动识别价格、信任、需求、竞品等异议类型
- 💡 **优秀案例对比**：针对薄弱环节推送标准话术参考
- 📱 **移动端适配**：响应式设计，完美支持手机浏览器
- 🔒 **隐私保护**：数据本地存储，不上传服务器

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

---

## 快速开始

### 环境要求

- Python 3.9+
- Node.js 16+
- 国产大模型API Key（推荐DeepSeek）

### 安装步骤

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
│   └── vite.config.js     # Vite配置
│
├── docs/                   # 文档目录
├── .gitignore             # Git忽略文件
└── README.md              # 项目说明
```

---

## 配置说明

### 后端配置（.env）

```env
# AI模型配置
DEFAULT_MODEL=deepseek-chat
MODEL_API_KEY=your_api_key_here
MODEL_API_BASE=https://api.deepseek.com/v1

# 对话配置
AI_RESPONSE_TIMEOUT=10
AI_TEMPERATURE=0.7
```

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

### Q: 如何获取AI模型的API Key？

A: 本项目推荐使用DeepSeek，访问 https://platform.deepseek.com/ 注册并获取API Key。

### Q: 支持哪些国产大模型？

A: 支持所有兼容OpenAI API格式的国产大模型，如：
- DeepSeek
- 智谱AI (ChatGLM)
- 百度文心一言
- 阿里通义千问
- 等等

### Q: 数据存储在哪里？

A: 所有数据都存储在本地：
- 对话记录：浏览器LocalStorage（前端）
- 角色配置：SQLite数据库（后端data目录）

### Q: 如何自定义角色和产品？

A: 可以通过以下方式：
1. 直接修改数据库（使用API接口）
2. 等待管理后台功能开发中

---

## 版本历史

### V1.2.0 (2025-12-30)
- ✅ 实现WebSocket实时对话
- ✅ 实现多维度AI评分
- ✅ 实现异议类型识别
- ✅ 实现优秀案例对比
- ✅ 移动端适配优化

### 计划功能
- ⏳ 管理后台界面
- ⏳ 产品文档自动解析
- ⏳ 语音对话功能
- ⏳ 数据导出功能

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
