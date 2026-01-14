# 🐳 Docker部署完整指南

## 📋 目录

- [系统要求](#系统要求)
- [项目结构](#项目结构)
- [快速部署](#快速部署)
- [详细配置](#详细配置)
- [常见问题](#常见问题)
- [运维管理](#运维管理)

---

## 系统要求

### 硬件要求
- **CPU**: 2核心及以上
- **内存**: 4GB及以上
- **磁盘**: 10GB可用空间

### 软件要求
- **操作系统**: Linux / macOS / Windows
- **Docker**: 20.10.0 及以上
- **Docker Compose**: 2.0.0 及以上

### 检查Docker环境

```bash
# 检查Docker版本
docker --version

# 检查Docker Compose版本
docker-compose --version

# 检查Docker服务状态
docker ps
```

---

## 项目结构

### Docker化后的完整项目结构

```
Insurance Q&A System/
├── docker-compose.yml          # ✨ Docker编排配置（新增）
├── .env.example                # ✨ 环境变量模板（新增）
├── .dockerignore               # ✨ Docker忽略文件（新增）
├── README.md                   # 项目说明
│
├── backend/                    # 后端服务
│   ├── Dockerfile             # ✨ 后端镜像构建文件（新增）
│   ├── .dockerignore          # ✨ 后端构建忽略文件（新增）
│   ├── main.py                # 应用入口
│   ├── requirements.txt       # Python依赖
│   └── app/                   # 应用代码
│       ├── api/               # API路由
│       ├── core/              # 核心配置
│       ├── models/            # 数据模型
│       └── services/          # 业务服务
│
├── frontend/                   # 前端服务
│   ├── Dockerfile             # ✨ 前端镜像构建文件（新增）
│   ├── .dockerignore          # ✨ 前端构建忽略文件（新增）
│   ├── nginx.conf             # ✨ Nginx配置文件（新增）
│   ├── package.json           # Node依赖
│   ├── vite.config.js         # Vite配置
│   └── src/                   # 源代码
│
├── docs/                       # 文档目录
│   └── ...
└── scripts/                    # 脚本目录
    └── ...
```

---

## 快速部署

### 步骤1：获取项目代码

```bash
# 克隆项目
git clone <your-repo-url>
cd "Insurance Q&A System"

# 或者如果是压缩包
unzip "Insurance Q&A System.zip"
cd "Insurance Q&A System"
```

### 步骤2：配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入必要的配置
vim .env
# 或使用其他编辑器：nano .env, notepad .env 等
```

**最少需要配置的变量**：

```env
# 必填：AI模型API密钥
MODEL_API_KEY=your_actual_api_key_here

# 可选：选择使用的AI模型
DEFAULT_MODEL=deepseek-chat
MODEL_API_BASE=https://api.deepseek.com/v1
```

### 步骤3：启动服务

```bash
# 构建并启动所有服务（后台运行）
docker-compose up -d

# 查看启动日志
docker-compose logs -f

# 等待看到以下日志表示启动成功：
# frontend | ... nginx started successfully
# backend | ... Application startup complete
```

### 步骤4：验证部署

```bash
# 检查容器状态
docker-compose ps

# 应该看到两个容器都是 "Up" 状态：
# NAME                      STATUS
# insurance-frontend        Up (healthy)
# insurance-backend         Up (healthy)
```

### 步骤5：访问应用

- **前端地址**: http://localhost (或 http://服务器IP)
- **后端API**: http://localhost:8000 (或 http://服务器IP:8000)
- **API文档**: http://localhost:8000/docs

---

## 详细配置

### AI模型配置说明

#### 推荐配置：DeepSeek（免费额度大）

```env
MODEL_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
DEFAULT_MODEL=deepseek-chat
MODEL_API_BASE=https://api.deepseek.com/v1
```

#### 其他可选模型

**通义千问**:
```env
DEFAULT_MODEL=qwen-plus
MODEL_API_BASE=https://dashscope.aliyuncs.com/compatible-mode/v1
```

**智谱AI (ChatGLM)**:
```env
DEFAULT_MODEL=glm-4
MODEL_API_BASE=https://open.bigmodel.cn/api/paas/v4
```

**Kimi (月之暗面)**:
```env
DEFAULT_MODEL=moonshot-v1-8k
MODEL_API_BASE=https://api.moonshot.cn/v1
```

### 端口配置

如果默认端口被占用，可以在 `docker-compose.yml` 中修改：

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 将8000改为8001

  frontend:
    ports:
      - "8080:80"    # 将80改为8080
```

### 数据持久化

数据库默认使用命名卷 `backend-data` 持久化（见 `docker-compose.yml`），容器内路径为 `/app/data`。
如需直接落盘到仓库目录，可改为 bind mount：

```yaml
volumes:
  - ./backend/data:/app/data
```

**种子数据库（首次部署带示例数据）**:
仓库内提供 `backend/data/insurance_practice.db`。如果使用默认的命名卷，需要先把种子数据库复制到卷里。
默认卷名通常是 `<项目目录名>_backend-data`（例如 `insurance-q-a-system_backend-data`）：

```bash
# 先确认卷名
docker volume ls

# 将种子数据库复制到卷（将 <volume_name> 替换为实际卷名）
docker run --rm -v <volume_name>:/app/data -v ${PWD}/backend/data:/seed busybox sh -c "cp /seed/insurance_practice.db /app/data/"
```

**备份数据**:
```bash
# 备份数据库
cp backend/data/insurance_practice.db backup_$(date +%Y%m%d).db
```

---

## 常见问题

### Q1: 构建失败 - "vite: Permission denied"

**解决方法**:

已通过以下方式解决：
1. ✅ 使用 Node.js 18 替代 Node.js 16
2. ✅ 在 Dockerfile 中添加权限设置
3. ✅ 使用多阶段构建

```bash
# 清理并重新构建
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Q2: 构建失败 - "crypto.getRandomValues is not a function"

**解决方法**:

已通过以下方式解决：
1. ✅ 升级到 Node.js 18（内置crypto polyfill）
2. ✅ 设置 `NODE_ENV=production`

```bash
# 如果仍有问题，清理缓存重试
docker system prune -a -f
docker-compose build --no-cache frontend
```

### Q3: API调用失败 - 连接AI模型超时

**检查步骤**:

```bash
# 1. 检查.env文件中的API_KEY是否正确
cat .env | grep MODEL_API_KEY

# 2. 检查网络连接
docker exec -it insurance-backend ping api.deepseek.com

# 3. 查看后端日志
docker-compose logs backend | grep -i error

# 4. 测试AI连接
docker exec -it insurance-backend python -c "
import asyncio
from app.services.ai_service import get_ai_service
result = asyncio.run(get_ai_service().test_connection())
print('连接测试结果:', result)
"
```

### Q4: 前端无法连接后端

**解决方法**:

```bash
# 检查网络配置
docker network inspect insurance-network

# 检查nginx配置
docker exec insurance-frontend cat /etc/nginx/conf.d/default.conf

# 测试从frontend容器访问backend
docker exec insurance-frontend wget -O- http://backend:8000/health
```

### Q5: 端口冲突

```bash
# 检查端口占用
netstat -tulpn | grep :80
netstat -tulpn | grep :8000

# 停止占用端口的服务或修改docker-compose.yml中的端口映射
```

### Q6: 容器启动失败

```bash
# 查看详细日志
docker-compose logs backend
docker-compose logs frontend

# 检查容器状态
docker ps -a

# 重启服务
docker-compose restart
```

---

## 运维管理

### 日常操作命令

#### 查看日志

```bash
# 查看所有服务日志（实时）
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 查看最近100行日志
docker-compose logs --tail=100 backend
```

#### 服务管理

```bash
# 停止服务
docker-compose stop

# 启动服务
docker-compose start

# 重启服务
docker-compose restart

# 重启特定服务
docker-compose restart backend

# 停止并删除容器
docker-compose down

# 停止并删除容器和数据卷（谨慎使用）
docker-compose down -v
```

#### 更新部署

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建镜像
docker-compose build

# 3. 重启服务（使用新镜像）
docker-compose up -d

# 或使用一键命令（无缓存重建）
docker-compose up -d --build --force-recreate
```

#### 进入容器调试

```bash
# 进入后端容器
docker exec -it insurance-backend bash

# 进入前端容器
docker exec -it insurance-frontend sh

# 在容器内执行命令
docker exec insurance-backend python -c "print('Hello')"
```

### 性能监控

#### 查看资源使用

```bash
# 查看容器资源使用情况
docker stats

# 查看特定容器
docker stats insurance-backend insurance-frontend
```

#### 健康检查

```bash
# 检查容器健康状态
docker inspect --format='{{.State.Health.Status}}' insurance-backend
docker inspect --format='{{.State.Health.Status}}' insurance-frontend

# 手动触发健康检查
curl http://localhost:8000/health
curl http://localhost/
```

### 数据备份与恢复

#### 备份

```bash
# 备份数据库
mkdir -p backups
cp backend/data/insurance_practice.db backups/backup_$(date +%Y%m%d_%H%M%S).db

# 备份环境配置
cp .env backups/env_backup_$(date +%Y%m%d).txt
```

#### 恢复

```bash
# 停止服务
docker-compose down

# 恢复数据库
cp backups/backup_20250105.db backend/data/insurance_practice.db

# 重启服务
docker-compose up -d
```

### 日志管理

```bash
# 清理旧日志（Docker日志文件）
docker-compose logs --tail=0 -f

# 限制日志大小（在docker-compose.yml中添加）
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

---

## 高级配置

### 使用外部数据库

如果要使用PostgreSQL替代SQLite：

```yaml
# 在docker-compose.yml中添加
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: insurance_practice
      POSTGRES_USER: insurance_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - insurance-network

  backend:
    environment:
      - DATABASE_URL=postgresql+asyncpg://insurance_user:your_password@postgres/insurance_practice
    depends_on:
      - postgres

volumes:
  postgres_data:
```

### 配置HTTPS（使用Let's Encrypt）

```bash
# 使用certbot获取SSL证书
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 修改nginx配置启用HTTPS
# 在frontend/nginx.conf中添加SSL配置
```

### 多实例部署

```yaml
# 修改docker-compose.yml，使用环境变量区分实例
services:
  backend:
    container_name: insurance-backend-${INSTANCE_ID:-prod}
    environment:
      - INSTANCE_ID=${INSTANCE_ID:-prod}
```

---

## 安全建议

### 1. 保护敏感信息

```bash
# 不要将.env文件提交到Git
echo ".env" >> .gitignore

# 设置.env文件权限
chmod 600 .env
```

### 2. 使用非root用户运行

已在Dockerfile中配置，容器内使用非特权用户。

### 3. 限制容器资源

```yaml
# 在docker-compose.yml中添加资源限制
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### 4. 定期更新镜像

```bash
# 更新基础镜像
docker-compose pull
docker-compose up -d
```

---

## 生产环境检查清单

### 部署前检查

- [ ] 已配置有效的 `MODEL_API_KEY`
- [ ] 已设置 `DEBUG=False`
- [ ] 已配置CORS正确域名
- [ ] 数据持久化路径已配置
- [ ] 端口映射无冲突
- [ ] 防火墙已开放必要端口
- [ ] 日志轮转已配置
- [ ] 备份策略已制定

### 部署后验证

- [ ] 前端页面可正常访问
- [ ] 后端API可正常调用
- [ ] WebSocket连接正常
- [ ] AI对话功能正常
- [ ] 评分功能正常
- [ ] 数据可正常保存
- [ ] 健康检查正常

---

## 故障排查流程图

```
问题出现
    ↓
检查容器状态
docker-compose ps
    ↓
查看日志
docker-compose logs -f
    ↓
    ├─ 容器未启动 → 检查端口/资源/配置
    ├─ 启动失败 → 查看构建日志 → 修复配置
    ├─ 运行时错误 → 进入容器调试 → 修复代码
    └─ 网络问题 → 检查DNS/防火墙/代理
    ↓
修复后重启
docker-compose restart
```

---

## 获取帮助

- 📖 查看项目文档: `docs/README.md`
- 🐛 提交问题: GitHub Issues
- 💬 技术支持: 联系项目维护者

---

## 附录

### A. 完整的docker-compose.yml示例

参考项目根目录下的 `docker-compose.yml` 文件

### B. 环境变量完整列表

参考 `.env.example` 文件

### C. 常用Docker命令速查

```bash
# 镜像相关
docker images                           # 查看镜像
docker rmi <image_id>                   # 删除镜像
docker system prune -a                  # 清理所有未使用的镜像

# 容器相关
docker ps                               # 查看运行中容器
docker ps -a                            # 查看所有容器
docker exec -it <container> bash        # 进入容器
docker logs <container>                 # 查看容器日志
docker stats                            # 查看资源使用

# 网络相关
docker network ls                       # 查看网络
docker network inspect <network>        # 查看网络详情

# 卷相关
docker volume ls                        # 查看卷
docker volume inspect <volume>          # 查看卷详情
```

---

**文档版本**: V1.0
**最后更新**: 2026-01-05
**适用版本**: V0.2.2+
**维护人员**: 项目开发组
