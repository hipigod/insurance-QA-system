# 保险销售智能陪练系统

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

## 快速开始（Docker）

```bash
cp .env.example .env
# 填写 MODEL_API_KEY

docker compose up -d
```

前端：http://localhost
后端健康检查：http://localhost:8000/api/v1/health

## 本地开发

后端：
```bash
cd backend
mvn -DskipTests package
java -jar target/qa-backend-0.1.0.jar
```

前端：
```bash
cd frontend
npm install
npm run dev
```

HMR 说明（仅开发环境）：如果通过非默认主机/端口访问 Vite（例如反代/8081），
请在 `npm run dev` 前设置以下环境变量：
```bash
VITE_DEV_PORT=8081
VITE_HMR_PORT=8081
VITE_HMR_HOST=localhost
```

## 环境变量

默认值参考 `.env.example`。

## 项目结构

```
backend/         # Spring Boot 后端
frontend/        # Vue 前端
docs/            # 文档
```
