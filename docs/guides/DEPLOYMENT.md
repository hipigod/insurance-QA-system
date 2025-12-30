# 部署指南

本文档详细介绍如何部署保险销售智能陪练系统。

---

## 目录

1. [开发环境部署](#开发环境部署)
2. [生产环境部署](#生产环境部署)
3. [数据库初始化](#数据库初始化)
4. [常见问题](#常见问题)

---

## 开发环境部署

### 前置要求

确保已安装以下软件：

- **Python**: 3.9 或更高版本
- **Node.js**: 16.x 或更高版本
- **Git**: 用于版本控制

### 步骤1: 获取代码

```bash
# 克隆仓库
git clone <repository-url>
cd Insurance Q&A System
```

### 步骤2: 后端部署

```bash
# 进入后端目录
cd backend

# 创建Python虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
copy .env.example .env  # Windows
# 或
cp .env.example .env    # Linux/Mac
```

编辑 `.env` 文件，填入您的配置：

```env
# 必填项
MODEL_API_KEY=sk-xxxxxxxxxxxxx

# 可选项（使用默认值即可）
DEFAULT_MODEL=deepseek-chat
MODEL_API_BASE=https://api.deepseek.com/v1
HOST=127.0.0.1
PORT=8000
```

### 步骤3: 前端部署

```bash
# 打开新终端
cd frontend

# 安装依赖
npm install
```

### 步骤4: 初始化数据库

```bash
# 在backend目录执行
cd backend
python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
```

### 步骤5: 启动服务

**启动后端**（终端1）：
```bash
cd backend
python main.py
```

看到以下信息表示启动成功：
```
🚀 保险销售智能陪练系统 v1.2.0 启动成功！
📍 API地址: http://127.0.0.1:8000/docs
```

**启动前端**（终端2）：
```bash
cd frontend
npm run dev
```

看到以下信息表示启动成功：
```
  VITE v5.0.11  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 步骤6: 访问应用

打开浏览器访问：http://localhost:5173

---

## 生产环境部署

### 方案1: 使用Docker（推荐）

#### 构建后端镜像

```bash
cd backend
docker build -t insurance-practice-backend .
```

#### 构建前端镜像

```bash
cd frontend
docker build -t insurance-practice-frontend .
```

#### 使用Docker Compose

在项目根目录创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MODEL_API_KEY=${MODEL_API_KEY}
      - MODEL_API_BASE=${MODEL_API_BASE}
    volumes:
      - ./backend/data:/app/data

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

启动：
```bash
docker-compose up -d
```

### 方案2: 传统部署

#### 后端部署

```bash
# 使用Gunicorn作为生产服务器
pip install gunicorn

# 启动
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### 前端部署

```bash
# 构建生产版本
cd frontend
npm run build

# 使用Nginx托管静态文件
# 将 dist 目录内容部署到Nginx
```

Nginx配置示例：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/insurance-practice/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # WebSocket代理
    location /ws {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 数据库初始化

### 自动初始化

首次启动后端时，系统会自动创建数据库表。

### 手动初始化数据

创建初始化脚本 `init_data.py`：

```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.models.models import CustomerRole, InsuranceProduct, ScoringDimension

async def init_demo_data():
    """初始化演示数据"""
    await init_db()

    async with AsyncSessionLocal() as session:
        # 创建客户角色
        roles = [
            CustomerRole(
                name="小白客户",
                description="对保险了解不多，需要耐心解释",
                difficulty="简单",
                system_prompt="你是一个对保险了解不多的普通客户..."
            ),
            CustomerRole(
                name="懂行客户",
                description="对保险有一定了解，会问专业问题",
                difficulty="困难",
                system_prompt="你是一个对保险产品有一定了解的客户..."
            ),
            CustomerRole(
                name="难缠客户",
                description="挑剔，提出各种异议，难以说服",
                difficulty="专家",
                system_prompt="你是一个挑剔难缠的客户..."
            )
        ]

        # 创建保险产品
        products = [
            InsuranceProduct(
                name="重疾险无忧版",
                product_type="重疾险",
                description="覆盖120种重疾，保费低保障高",
                coverage="120种重疾+20种中症+40种轻症",
                premium_range="3000-10000元/年",
                target_audience="18-50岁成年人",
                detailed_info="..."
            ),
            InsuranceProduct(
                name="百万医疗险",
                product_type="医疗险",
                description="百万保额，看病不愁",
                coverage="住院医疗+门诊手术+特殊门诊",
                premium_range="300-1000元/年",
                target_audience="0-60岁人群",
                detailed_info="..."
            )
        ]

        # 创建评分维度
        dimensions = [
            ScoringDimension(
                name="沟通能力",
                description="语言表达、倾听能力、共情能力",
                weight=25.0,
                evaluation_prompt="评估表达是否清晰流畅，是否善于倾听..."
            ),
            ScoringDimension(
                name="有效营销",
                description="需求挖掘、价值传递、异议处理",
                weight=25.0,
                evaluation_prompt="评估是否准确挖掘客户需求..."
            ),
            ScoringDimension(
                name="产品熟练度",
                description="产品知识准确性、条款解释能力",
                weight=25.0,
                evaluation_prompt="评估产品知识是否准确..."
            ),
            ScoringDimension(
                name="异议处理能力",
                description="异议识别、应对策略、说服效果",
                weight=25.0,
                evaluation_prompt="评估异议识别和应对能力..."
            )
        ]

        for role in roles:
            session.add(role)

        for product in products:
            session.add(product)

        for dimension in dimensions:
            session.add(dimension)

        await session.commit()
        print("✅ 演示数据初始化成功！")

if __name__ == "__main__":
    asyncio.run(init_demo_data())
```

运行初始化：
```bash
python init_data.py
```

---

## 常见问题

### 1. API调用失败

**问题**: 提示"API Key未配置"或"调用失败"

**解决方案**:
- 检查 `.env` 文件中的 `MODEL_API_KEY` 是否正确
- 确认API Key有效且有足够的额度
- 检查网络连接是否正常

### 2. WebSocket连接失败

**问题**: 对话页面无法连接

**解决方案**:
- 确认后端服务已启动
- 检查防火墙设置
- 查看浏览器控制台错误信息

### 3. 数据库错误

**问题**: 提示"表不存在"

**解决方案**:
```bash
# 重新初始化数据库
cd backend
rm data/insurance_practice.db  # 删除旧数据库
python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
python init_data.py  # 重新导入数据
```

### 4. 前端构建失败

**问题**: `npm install` 或 `npm run build` 失败

**解决方案**:
```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm install

# 或使用淘宝镜像
npm install --registry=https://registry.npmmirror.com
```

### 5. 端口被占用

**问题**: 启动时提示端口已被使用

**解决方案**:

**Windows**:
```bash
# 查找占用进程
netstat -ano | findstr :8000
# 结束进程
taskkill /PID <进程ID> /F
```

**Linux/Mac**:
```bash
# 查找并结束进程
lsof -ti:8000 | xargs kill -9
```

或修改 `.env` 文件中的端口配置。

---

## 性能优化建议

1. **后端优化**:
   - 使用生产级ASGI服务器（Gunicorn + Uvicorn）
   - 启用数据库连接池
   - 添加缓存机制（Redis）

2. **前端优化**:
   - 启用Gzip压缩
   - 配置CDN加速
   - 代码分割和懒加载

3. **数据库优化**:
   - 添加适当索引
   - 定期清理历史数据
   - 考虑迁移到PostgreSQL

---

## 安全建议

1. **API Key安全**:
   - 不要将 `.env` 文件提交到Git
   - 定期更换API Key
   - 使用环境变量管理敏感信息

2. **数据备份**:
   - 定期备份SQLite数据库文件
   - 建议每天自动备份

3. **HTTPS**:
   - 生产环境必须使用HTTPS
   - 配置SSL证书（Let's Encrypt免费）

---

## 监控和日志

### 后端日志

后端日志输出到控制台，可以使用以下方式管理：

```bash
# 保存到文件
python main.py > logs/app.log 2>&1

# 使用日志管理工具
nohup python main.py > logs/app.log 2>&1 &
```

### 前端错误监控

集成Sentry等错误监控服务（可选）。

---

## 更新部署

### 拉取最新代码

```bash
git pull origin main
```

### 后端更新

```bash
cd backend
pip install -r requirements.txt --upgrade
# 重启服务
```

### 前端更新

```bash
cd frontend
npm install
npm run build
# 重新部署dist目录
```

---

如有其他问题，请查看 [README.md](README.md) 或提交Issue。
