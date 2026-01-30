# 保险销售智能陪练系统
版本：V0.3

基于 AI 的保险销售训练平台，前端为 Vue 3，后端为 Java Spring Boot。

## 技术栈

后端：
- Spring Boot 3.x（Web、WebSocket）
- Spring Data JPA
- SQLite
- OpenAI 兼容 API 客户端（如 DeepSeek）

前端：
- Vue 3 + Vite
- Element Plus
- Pinia

部署：
- Docker + Docker Compose
- Nginx 反向代理

## API 概览

基础路径：`/api/v1`
WebSocket：`/ws/dialogue`

示例：
- `GET /api/v1/roles`
- `POST /api/v1/dialogues`
- `POST /api/v1/dialogues/score`

WebSocket 事件：
- 客户端：`{ "type": "subscribe", "sessionId": "..." }`
- 客户端：`{ "type": "chat", "sessionId": "...", "message": "..." }`
- 客户端：`{ "type": "end", "sessionId": "..." }`
- 服务端：`{ "type": "message", "sessionId": "...", "role": "assistant", "content": "..." }`
- 服务端：`{ "type": "score", "sessionId": "...", "data": { ... } }`

## 快速开始

### 前置要求
- Docker
- Docker Compose
- AI 模型 API Key（支持 OpenAI 兼容接口，如 DeepSeek）

### 启动步骤

1. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，填入 MODEL_API_KEY
```

2. 启动服务
```bash
docker compose up -d
```

3. 访问应用
- 前端：http://localhost
- 后端健康检查：http://localhost:8000/api/v1/health

### 停止服务
```bash
docker compose down
```

### 清理数据（可选）
```bash
docker compose down -v  # 删除数据库卷
```

## 本地开发

### 后端开发
```bash
cd backend
mvn clean package -DskipTests
java -jar target/qa-backend-0.1.0.jar
```

### 前端开发
```bash
cd frontend
npm install
npm run dev
```

前端开发服务器默认运行在 http://localhost:5173

### HMR 配置（可选）
如果需要自定义 Vite 开发服务器端口：
```bash
VITE_DEV_PORT=8081 npm run dev
```

## 环境变量

主要环境变量（详见 `.env.example`）：
- `MODEL_API_KEY` - AI 模型 API 密钥（必需）
- `MODEL_API_BASE` - API 基础 URL
- `MODEL_NAME` - 模型名称
- `JAVA_OPTS` - JVM 参数

## 项目结构

```
.
├── backend/              # Spring Boot 后端
│   ├── src/             # 源代码
│   └── pom.xml          # Maven 配置
├── frontend/            # Vue 3 前端
│   ├── src/            # 源代码
│   └── package.json    # NPM 配置
├── docs/               # 文档
│   ├── guides/         # 使用指南
│   ├── problemsolve/   # 问题排查记录
│   └── 一键远程部署/   # 远程部署方案
├── docker-compose.yml  # Docker 编排配置
├── .env.example        # 环境变量示例
└── README.md           # 项目说明
```

## 文档

- [部署与运行指南](docs/guides/DEPLOY_RUN.md)
- [模型配置指南](docs/guides/MODEL_CONFIG_GUIDE.md)
- [预设数据说明](docs/guides/预设数据说明.md)
- [远程部署方案](docs/一键远程部署/REMOTE_DEPLOY.md)
- [问题排查记录](docs/problemsolve/)
