# Web服务器部署指南

> 保险销售智能陪练系统 - 生产环境部署完整教程

## 📋 目录

- [部署架构](#部署架构)
- [方案一：传统服务器部署](#方案一传统服务器部署推荐)
- [方案二：Docker容器部署](#方案二docker容器部署)
- [方案三：云平台部署](#方案三云平台部署)
- [部署验证](#部署验证)
- [常见问题](#常见问题)
- [性能优化](#性能优化)

---

## 部署架构

### 系统架构图

```
┌─────────────────────────────────────────┐
│           用户浏览器                     │
│  https://your-domain.com              │
└──────────────┬──────────────────────────┘
               │
               ↓
┌─────────────────────────────────────────┐
│       Nginx 反向代理服务器               │
│       (端口 80/443)                    │
├──────────────┬──────────────────────────┤
│              │                          │
│   静态文件   │      API代理              │
│   /          │      /api/*               │
│   /ws        │      /ws/*                │
│              │                          │
└──────┬───────┴──────────┬───────────────┘
       │                  │
       ↓                  ↓
┌──────────────┐  ┌──────────────────┐
│   前端静态    │  │   后端服务       │
│   (构建产物)  │  │   FastAPI        │
│   Nginx托管   │  │   端口8000       │
│              │  │   Systemd管理    │
└──────────────┘  └──────────┬───────┘
                            │
                            ↓
                  ┌──────────────────┐
                  │   SQLite数据库    │
                  │   backend/data/   │
                  └──────────────────┘
```

### 技术栈说明

**前端**:
- Vue 3 + Vite
- Element Plus UI
- 生产构建: 静态HTML/CSS/JS文件

**后端**:
- Python 3.9+
- FastAPI 异步框架
- SQLite 数据库
- WebSocket 实时通信

**Web服务器**:
- Nginx (推荐)
  - 静态文件托管
  - 反向代理
  - WebSocket代理
  - SSL/HTTPS支持
- Apache (备选)

---

## 方案一：传统服务器部署 (推荐)

### 适用场景

- ✅ VPS (虚拟专用服务器)
- ✅ 云服务器 (阿里云、腾讯云等)
- ✅ 物理服务器
- ✅ 需要完全控制服务器

### 环境要求

| 组件 | 版本要求 | 用途 |
|------|---------|------|
| Python | 3.9+ | 运行后端服务 |
| Node.js | 16+ | 构建前端 |
| Nginx | 1.18+ | Web服务器 |
| Git | 最新版 | 代码管理 |
| 系统 | Ubuntu 20.04+ / Debian 10+ | 推荐(Linux) |

### 步骤1: 准备服务器环境

#### 1.1 更新系统

```bash
# Ubuntu/Debian
sudo apt update
sudo apt upgrade -y

# CentOS/RHEL
sudo yum update -y
```

#### 1.2 安装Python 3.9+

```bash
# Ubuntu/Debian
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa-python3.9 -y
sudo apt update
sudo apt install python3.9 python3.9-venv python3-pip -y

# 验证安装
python3.9 --version
```

#### 1.3 安装Node.js 16+

```bash
# 使用NodeSource仓库
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs

# 验证安装
node --version
npm --version
```

#### 1.4 安装Nginx

```bash
sudo apt install nginx -y

# 启动Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# 验证安装
sudo nginx -v
```

#### 1.5 安装Git

```bash
sudo apt install git -y
```

### 步骤2: 部署应用代码

#### 2.1 克隆代码

```bash
# 创建项目目录
sudo mkdir -p /var/www
cd /var/www

# 克隆代码
sudo git clone https://github.com/hipigod/insurance-QA-system.git
cd insurance-QA-system

# 设置权限
sudo chown -R $USER:$USER /var/www/insurance-QA-system
```

#### 2.2 配置后端

```bash
# 进入后端目录
cd backend

# 创建Python虚拟环境
python3.9 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
nano .env
```

**编辑.env文件**:

```env
# 应用配置
APP_NAME=保险销售智能陪练系统
APP_VERSION=0.2.1
DEBUG=False

# 服务器配置
HOST=127.0.0.1
PORT=8000

# AI模型配置 - DeepSeek(推荐)
DEFAULT_MODEL=deepseek-chat
MODEL_API_KEY=your_api_key_here
MODEL_API_BASE=https://api.deepseek.com/v1

# 对话配置
MAX_DIALOGUE_ROUNDS=20
AI_RESPONSE_TIMEOUT=25
AI_TEMPERATURE=0.7
```

**重要**: 修改`MODEL_API_KEY`为您的真实API Key

```bash
# 初始化数据库
python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"

# 测试运行
python main.py

# 看到以下输出表示成功:
# "保险销售智能陪练系统 v0.2.1 启动成功!"
# "Uvicorn running on http://127.0.0.1:8000"

# 按Ctrl+C停止测试
```

#### 2.3 构建前端

```bash
# 打开新终端,进入前端目录
cd /var/www/insurance-QA-system/frontend

# 安装依赖
npm install

# 修改API地址(如果需要)
nano src/api/index.js
# 确保 baseURL: '/api' (使用相对路径)

# 构建生产版本
npm run build

# 验证构建
ls dist/
# 应该看到: index.html, assets/ 等文件
```

### 步骤3: 配置Systemd服务

创建后端服务文件,让后端在后台持续运行。

```bash
# 创建Systemd服务文件
sudo nano /etc/systemd/system/insurance-qa-backend.service
```

**服务配置内容**:

```ini
[Unit]
Description=Insurance QA System Backend
Documentation=https://github.com/hipigod/insurance-QA-system
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/insurance-QA-system/backend
Environment="PATH=/var/www/insurance-QA-system/backend/venv/bin"
ExecStart=/var/www/insurance-QA-system/backend/venv/bin/python main.py
Restart=always
RestartSec=10

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=insurance-qa-backend

[Install]
WantedBy=multi-user.target
```

```bash
# 设置权限
sudo chown -R www-data:www-data /var/www/insurance-QA-system

# 重载Systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start insurance-qa-backend

# 设置开机自启
sudo systemctl enable insurance-qa-backend

# 查看服务状态
sudo systemctl status insurance-qa-backend

# 查看日志
sudo journalctl -u insurance-qa-backend -f
```

### 步骤4: 配置Nginx

#### 4.1 创建站点配置

```bash
# 创建Nginx配置文件
sudo nano /etc/nginx/sites-available/insurance-qa
```

**Nginx配置内容**:

```nginx
# HTTP服务器配置
server {
    listen 80;
    server_name your-domain.com;  # 改为您的域名或服务器IP

    # 字符集
    charset utf-8;

    # 日志
    access_log /var/log/nginx/insurance-qa-access.log;
    error_log /var/log/nginx/insurance-qa-error.log;

    # 前端静态文件
    location / {
        root /var/www/insurance-QA-system/frontend/dist;
        try_files $uri $uri/ /index.html;

        # 缓存静态资源
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # WebSocket代理
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

        # WebSocket超时设置
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }

    # 禁止访问隐藏文件
    location ~ /\. {
        deny all;
    }
}
```

#### 4.2 启用配置

```bash
# 创建符号链接
sudo ln -s /etc/nginx/sites-available/insurance-qa /etc/nginx/sites-enabled/

# 删除默认配置(可选)
# sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 如果测试通过,重载Nginx
sudo systemctl reload nginx

# 如果完全重启
sudo systemctl restart nginx
```

### 步骤5: 配置防火墙

```bash
# UFW (Ubuntu防火墙)
sudo ufw allow 'Nginx Full'
sudo ufw enable

# firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# 如果云服务器,需要在云平台控制台开放端口:
# - 80 (HTTP)
# - 443 (HTTPS)
# - 22 (SSH)
```

### 步骤6: 配置HTTPS (可选但推荐)

#### 使用Let's Encrypt免费SSL证书

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书
sudo certbot --nginx -d your-domain.com

# 按提示操作:
# 1. 输入邮箱
# 2. 同意服务条款
# 3. 选择重定向(HTTP → HTTPS)

# Certbot会自动修改Nginx配置
sudo systemctl reload nginx

# 设置自动续期
sudo certbot renew --dry-run
```

---

## 方案二:Docker容器部署

### 适用场景

- ✅ 容器化部署
- ✅ 微服务架构
- ✅ 快速扩容
- ✅ 开发/测试环境

### 环境要求

- Docker 20.10+
- Docker Compose 1.29+

### 步骤1: 安装Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 验证安装
docker --version
docker-compose --version
```

### 步骤2: 创建Dockerfile

#### 后端Dockerfile

```bash
cd /var/www/insurance-QA-system/backend
nano Dockerfile
```

```dockerfile
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建数据目录
RUN mkdir -p /app/data

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "main.py"]
```

#### 前端Dockerfile

```bash
cd ../frontend
nano Dockerfile
```

```dockerfile
# 构建阶段
FROM node:16-alpine as builder

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制源代码
COPY . .

# 构建生产版本
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 从构建阶段复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制Nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**创建前端Nginx配置**:

```bash
cd frontend
nano nginx.conf
```

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /ws {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 步骤3: 创建docker-compose.yml

```bash
cd /var/www/insurance-QA-system
nano docker-compose.yml
```

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: insurance-qa-backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      - MODEL_API_KEY=${MODEL_API_KEY}
      - DEFAULT_MODEL=deepseek-chat
      - MODEL_API_BASE=https://api.deepseek.com/v1
      - AI_RESPONSE_TIMEOUT=25
      - AI_TEMPERATURE=0.7
    volumes:
      - ./backend/data:/app/data
    networks:
      - insurance-qa-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/docs"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: insurance-qa-frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - insurance-qa-network

networks:
  insurance-qa-network:
    driver: bridge
```

### 步骤4: 部署Docker服务

```bash
# 创建环境变量文件
cat > .env <<EOF
MODEL_API_KEY=your_api_key_here
EOF

# 构建并启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 查看运行状态
docker-compose ps
```

### Docker管理命令

```bash
# 查看日志
docker-compose logs -f backend
docker-compose logs -f frontend

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 更新服务
docker-compose up -d --build

# 查看资源使用
docker stats
```

---

## 方案三:云平台部署

### 3.1 Vercel + Railway 部署

#### 适用场景
- ✅ 快速部署
- ✅ 免费套餐
- ✅ 自动HTTPS
- ✅ 全球CDN

#### 步骤1: 部署前端到Vercel

```bash
# 安装Vercel CLI
npm install -g vercel

# 登录
vercel login

# 部署
cd frontend
vercel

# 按提示操作:
# 1. 设置项目名称
# 2. 选择框架 (Vue)
# 3. 自动检测配置
```

#### 步骤2: 部署后端到Railway

```bash
# 访问 https://railway.app
# 点击 "New Project"
# 选择 "Deploy from GitHub repo"
# 选择仓库: hipigod/insurance-QA-system
# 配置环境变量:
#   - MODEL_API_KEY
#   - DEFAULT_MODEL
#   - MODEL_API_BASE
# 点击 "Deploy"
```

### 3.2 Render部署 (全栈)

#### 步骤1: 准备代码

创建`render.yaml`:

```yaml
services:
  - type: web
    name: insurance-qa-backend
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python main.py
    envVars:
      - key: MODEL_API_KEY
        sync: false
      - key: DEFAULT_MODEL
        value: deepseek-chat
      - key: MODEL_API_BASE
        value: https://api.deepseek.com/v1
    disk:
      name: data
      mountPath: /app/data

  - type: web
    name: insurance-qa-frontend
    runtime: static
    buildCommand: npm run build
    publishDir: frontend/dist
```

#### 步骤2: 部署

1. 访问 https://render.com
2. 连接GitHub仓库
3. 选择项目并配置
4. 点击"Deploy"

---

## 部署验证

### 功能检查清单

#### 1. 基础访问
- [ ] 前端页面可访问: http://your-domain.com
- [ ] 页面加载正常,无404错误
- [ ] 静态资源(CSS/JS)加载正常

#### 2. API功能
- [ ] API接口可访问: http://your-domain.com/api/
- [ ] 角色列表API正常
- [ ] 产品列表API正常

#### 3. WebSocket功能
- [ ] WebSocket连接正常
- [ ] 可以开始对话
- [ ] AI响应正常

#### 4. 完整流程测试
- [ ] 选择角色和产品
- [ ] 开始对话练习
- [ ] 进行多轮对话
- [ ] 结束对话
- [ ] 评分正常
- [ ] 跳转到结果页面
- [ ] 查看历史记录

#### 5. 管理后台
- [ ] 管理后台可访问
- [ ] 数据加载正常
- [ ] 增删改查功能正常

### 性能测试

```bash
# 使用ab测试
ab -n 100 -c 10 http://your-domain.com/

# 使用curl测试
curl -I http://your-domain.com
curl http://your-domain.com/api/roles/
```

---

## 常见问题

### Q1: 502 Bad Gateway

**原因**: 后端服务未启动或端口配置错误

**解决**:
```bash
# 检查后端服务状态
sudo systemctl status insurance-qa-backend

# 查看后端日志
sudo journalctl -u insurance-qa-backend -f

# 重启后端服务
sudo systemctl restart insurance-qa-backend
```

### Q2: WebSocket连接失败

**原因**: Nginx WebSocket代理配置错误

**解决**:
```bash
# 检查Nginx配置
cat /etc/nginx/sites-available/insurance-qa

# 确保包含以下配置:
location /ws {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}

# 重载Nginx
sudo systemctl reload nginx
```

### Q3: 静态资源404

**原因**: 前端构建路径错误

**解决**:
```bash
# 检查dist目录
ls -la /var/www/insurance-QA-system/frontend/dist/

# 重新构建
cd /var/www/insurance-QA-system/frontend
npm run build

# 检查Nginx配置中的root路径
```

### Q4: AI调用失败

**原因**: API Key未配置或无效

**解决**:
```bash
# 检查环境变量
sudo cat /etc/systemd/system/insurance-qa-backend.service

# 检查.env文件
cat /var/www/insurance-QA-system/backend/.env

# 修改API Key后重启服务
sudo systemctl restart insurance-qa-backend
```

### Q5: 端口被占用

**原因**: 8000端口已被其他程序使用

**解决**:
```bash
# 查看端口占用
sudo lsof -i :8000

# 杀死占用进程
sudo kill -9 <PID>

# 或者修改后端端口
nano /var/www/insurance-QA-system/backend/.env
# 修改 PORT=8001
```

---

## 性能优化

### 1. 启用Gzip压缩

在Nginx配置中添加:

```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_types text/plain text/css text/xml text/javascript
           application/json application/javascript application/xml+rss
           application/rss+xml font/truetype font/opentype
           application/vnd.ms-fontobject image/svg+xml;
```

### 2. 配置缓存

```nginx
# 静态资源缓存
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}

# API响应缓存(可选)
location /api/roles/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_cache_valid 200 5m;
}
```

### 3. 启用HTTP/2

```nginx
listen 443 ssl http2;
```

### 4. 优化后端性能

```bash
# 使用Gunicorn + Uvicorn worker
pip install gunicorn

# 修改启动命令
ExecStart=/var/www/insurance-QA-system/backend/venv/bin/gunicorn main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000
```

---

## 监控和日志

### 查看应用日志

```bash
# 后端日志
sudo journalctl -u insurance-qa-backend -f

# Nginx访问日志
sudo tail -f /var/log/nginx/insurance-qa-access.log

# Nginx错误日志
sudo tail -f /var/log/nginx/insurance-qa-error.log
```

### 设置日志轮转

```bash
sudo nano /etc/logrotate.d/insurance-qa
```

```
/var/log/nginx/insurance-qa-*.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        systemctl reload nginx > /dev/null 2>&1 || true
    endscript
}
```

---

## 更新部署

### 更新应用代码

```bash
# 1. 拉取最新代码
cd /var/www/insurance-QA-system
git pull

# 2. 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart insurance-qa-backend

# 3. 更新前端
cd ../frontend
npm install
npm run build
sudo systemctl reload nginx
```

### 回滚版本

```bash
# 查看提交历史
git log --oneline

# 回滚到指定版本
git checkout <commit-hash>

# 重新部署
# (重复部署步骤)
```

---

## 安全建议

### 1. 配置防火墙

```bash
# 只开放必要端口
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. 定期更新

```bash
# 定期更新系统包
sudo apt update && sudo apt upgrade -y

# 更新Python依赖
cd /var/www/insurance-QA-system/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

### 3. 数据备份

```bash
# 创建备份脚本
cat > /var/www/insurance-QA-system/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/www/backups/insurance-qa"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# 备份数据库
cp /var/www/insurance-QA-system/backend/data/*.db $BACKUP_DIR/data_$DATE.db

# 保留最近7天的备份
find $BACKUP_DIR -type f -mtime +7 -delete
EOF

chmod +x /var/www/insurance-QA-system/backup.sh

# 添加到crontab
crontab -e
# 每天凌晨2点备份
0 2 * * * /var/www/insurance-QA-system/backup.sh
```

---

## 联系支持

- **GitHub Issues**: https://github.com/hipigod/insurance-QA-system/issues
- **文档**: 详见项目README.md

---

**🎉 祝您部署成功!**
