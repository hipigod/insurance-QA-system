# 保险销售智能陪练系统 V0.3.0

> AI驱动的保险销售能力提升平台 —— 真实产品、有情绪的客户、严格的考官

## 项目简介

本项目是一个面向保险销售人员的AI智能陪练系统，通过模拟真实客户对话场景，帮助销售人员提升沟通能力、产品知识和营销技巧，并提供AI驱动的多维度能力评估。

在线演示：https://insurance.hipigod.top

### 核心功能

- 🤖 **AI对话练习**：7种情绪化客户角色（各有家庭背景、喜好厌恶、耐心阈值），反应接近真人
- 📞 **客户挂断机制**：连续敷衍或误导3次，客户会表达不满并挂断，自动转入评分
- 📊 **多维度严格评分**：需求挖掘、产品说明、异议处理、促成能力4维度，五档锚点定档+一票否决（编造产品信息0-20分、被挂断促成≤30分）
- 🔧 **多模型管理**：管理后台配置多个大模型（落盘服务器配置文件），开始练习时自由选择，支持连通性测试
- 📋 **真实产品资料**：内置2026年在售产品数据（小状元2号教育金/达尔文11号重疾/蓝医保百万医疗/定海柱8号定寿），客户问题围绕真实条款展开
- 🗂️ **练习历史服务端存储**：评分自动落库，跨设备、清缓存不丢失
- 💡 **优秀案例对比**：针对薄弱环节推送标准话术参考
- ⚙️ **管理后台**：角色、产品、评分维度、案例、模型配置一站式管理
- 🐳 **Docker部署**：一键编排，含低内存环境适配方案

### 技术栈

**后端**：
- FastAPI - 现代异步Web框架
- SQLite - 轻量级数据库
- WebSocket - 实时双向通信
- OpenAI SDK - 兼容国产大模型API（DeepSeek/通义千问等）

**前端**：
- Vue 3 + Vite + Element Plus + Pinia

**部署**：
- Docker + Docker Compose + Nginx

---

## 快速开始

### 部署方式选择

#### 🐳 方式一：Docker 部署（推荐）

**环境要求**：
- Docker 已安装并运行
- 兼容 OpenAI API 的大模型 API Key（推荐 DeepSeek）

**快速启动**：
```bash
# 1. 克隆项目
git clone https://github.com/hipigod/insurance-QA-system.git
cd insurance-QA-system

# 2. 启动（.env 仅需保留对话参数，模型在管理后台配置）
docker compose up -d

# 3. 初始化预设数据（首次运行，幂等可重复执行）
docker exec insurance-backend sh -c "cd /app && PYTHONPATH=/app python /tmp/init.py" 2>/dev/null || \
docker cp scripts/init_demo_data.py insurance-backend:/tmp/ && \
docker exec insurance-backend sh -c "cd /app && PYTHONPATH=/app python /tmp/init_demo_data.py"

# 4. 内容调优（真实产品/情绪角色/严格评分维度，幂等）
docker cp scripts/tune_content.py insurance-backend:/tmp/ && \
docker exec insurance-backend sh -c "cd /app && PYTHONPATH=/app python /tmp/tune_content.py"

# 5. 打开系统 → 管理后台 → 模型管理 → 添加模型（API Key + 接口地址）
```

**访问地址**：
- 前端：http://localhost
- 后端 API 文档：http://localhost:8000/docs

**低内存服务器注意**（≤2G）：
前端镜像采用预构建模式（本地 `npm run build` 后将 `dist/` 同步到服务器再构建镜像），避免容器内 `npm ci` OOM。资源充足环境可使用 `frontend/Dockerfile.build` 在容器内完成构建。

#### 💻 方式二：本地开发模式

**环境要求**：Python 3.9+、Node.js 16+

```bash
# 后端
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py          # http://127.0.0.1:8000

# 前端（新终端）
cd frontend
npm install
npm run dev             # http://localhost:5173
```

启动后进入 管理后台 → 模型管理 添加大模型配置。

---

## 配置说明

### 大模型配置（重要变更）

自 V0.3.0 起，大模型不再通过环境变量配置。启动系统后在 **管理后台 → 模型管理** 中添加：
- 模型名称（如 deepseek-chat / qwen-plus）
- 提供商
- API Key（保存后仅显示掩码，编辑留空表示沿用）
- API 地址（如 https://api.deepseek.com/v1）

模型配置持久化于服务器 `data/model_config.json`，支持多模型并存、启用禁用、连通性测试。开始对话练习时自由选择。

### 对话参数（.env）

```env
AI_RESPONSE_TIMEOUT=25  # AI响应超时(秒)
AI_TEMPERATURE=0.7      # AI创意度(0-1)
MAX_DIALOGUE_ROUNDS=20  # 最大对话轮次
```

---

## 使用指南

### 1. 选择场景
选择客户角色（7种：小白/理性分析/价格敏感/怀疑抗拒/犹豫/懂行/难缠）、保险产品、对话模型。

### 2. 对话练习
- AI客户主动打招呼，带有角色情绪与偏好
- 客户会围绕真实产品条款提问、比价、质疑
- **注意**：敷衍、答非所问、编造信息会消耗客户耐心，累计3次将被挂断
- 全程对话历史参与情绪记忆，长对话下客户的耐心是持续累计的

### 3. 评分报告
- 结束对话（或被挂断）后自动评分
- 五档锚点严格评分：乱答会被打回原形（实测瞎答总分个位数）
- 一票否决：编造产品信息、被客户挂断均有对应维度严惩
- 每个维度的评价引用对话原文佐证

### 4. 练习历史
- 评分结果与完整对话自动保存到服务端数据库
- 跨设备访问、清浏览器缓存不影响历史记录

---

## 常见问题

### Q: 如何获取大模型 API Key？
A: 推荐 DeepSeek（https://platform.deepseek.com/），也支持所有兼容 OpenAI API 的国产大模型（通义千问、智谱、Kimi 等）。

### Q: 数据存储在哪里？
A: 角色配置、产品信息、评分维度、练习记录均存储于 SQLite 数据库（Docker 命名卷 `backend-data` 持久化）；模型配置存储于 `data/model_config.json`。练习历史在服务端，与浏览器缓存无关。

### Q: 如何自定义角色和产品？
A: 管理后台支持增删改查。修改后立即生效，无需重启。

### Q: 客户挂断是怎么回事？
A: 每个角色有耐心设定，销售人员连续出现敷衍、答非所问、编造信息、强行催单等行为，客户会逐渐不满并最终挂断结束对话。挂断后自动评分，促成能力维度会被重罚。这是陪练的核心压力设计。

---

## 版本历史

### V0.3.0 (2026-09-15)

**模型管理重构**
- 🗑️ 移除内置默认模型（.env底座配置），模型统一在管理后台配置
- 💾 模型配置落盘 `data/model_config.json`（原子写入，旧DB配置自动迁移）
- 🔀 多模型并存，开始练习时自由选择，会话绑定模型全程使用
- 🔌 新增模型连通性测试，API Key 掩码回显（留空编辑表示沿用）

**练习历史修复**
- 🐛 修复生产环境 WebSocket 地址写死 127.0.0.1 导致对话评分链路全断
- 🐛 修复评分后记录不落库（此前仅存浏览器 localStorage 且只保留10条）
- 📦 记录改存服务端 SQLite，跨设备不丢失

**稳定性**
- 🐛 修复推理型模型评分卡死（思考耗尽token致空回复）：max_tokens 8000/超时120s/空返回分类报错
- 🐛 修复评分 JSON 解析过脆：代码块+大括号双定位稳健提取
- 🐛 修复长对话客户失忆：对话历史窗口从5条放开为全量

**内容全面调优**
- 📋 产品换真实在售数据：小状元2号教育金/达尔文11号重疾/蓝医保百万医疗/定海柱8号定寿
- 😤 7个角色情绪化重写：家庭背景、喜好厌恶、耐心挂断规则
- 📏 评分严格化：五档锚点+一票否决，乱答总分个位数
- 🐛 修复详细产品资料未传给AI的问题

**部署适配**
- 🐳 前端预构建镜像模式（低内存服务器适配），原方案保留为 Dockerfile.build
- 🔧 init 脚本幂等化（同名跳过），杜绝重复灌数据
- 🔒 backend/.dockerignore 排除本地数据库防污染镜像

### V0.2.2 (2026-01-07)
- 🐳 Docker部署优化、一键部署、预设数据、配置简化

### V0.2.1 (2025-12-31)
- 🐛 修复评分跳转Bug、超时配置、调试日志

### V0.2.0 (2025-12-31)
- ✅ 管理后台、超时优化、错误处理改进

### V1.2.0 (2025-12-30)
- ✅ WebSocket实时对话、多维度AI评分、异议识别、优秀案例对比

### 计划功能
- ⏳ 语音对话
- ⏳ 练习数据导出与统计分析
- ⏳ 用户系统与团队管理

---

## 贡献指南

欢迎提交Issue和Pull Request！

---

## 许可证

MIT License

---

**🚀 立即开始，在真实压力下提升您的保险销售能力！**
