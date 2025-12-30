# 快速启动指南 🚀

> 5分钟启动保险销售智能陪练系统

---

## 前置准备

在开始之前，请确保您已安装：

- ✅ **Python 3.9+** - [下载地址](https://www.python.org/downloads/)
- ✅ **Node.js 16+** - [下载地址](https://nodejs.org/)
- ✅ **Git** - [下载地址](https://git-scm.com/)
- ✅ **DeepSeek API Key** - [获取地址](https://platform.deepseek.com/)

> 💡 **提示**: 检查是否安装成功：
> - 打开命令行，输入 `python --version`
> - 输入 `node --version`
> - 输入 `git --version`

---

## 🎯 超快速启动（推荐）

如果您不想了解细节，只想快速运行，按照以下步骤操作：

### 步骤1: 配置后端

```bash
# 进入后端目录
cd backend

# 复制环境配置文件
# Windows: 在文件管理器中打开，复制 .env.example 为 .env
# Mac/Linux: 执行以下命令
cp .env.example .env

# 编辑 .env 文件，填入您的 API_KEY
# MODEL_API_KEY=sk-xxxxxxxxxxxxx  ← 在这里填入您的API密钥

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化演示数据
python ../init_demo_data.py
```

看到以下信息表示成功：
```
🎉 演示数据初始化完成！
   - 客户角色: 4 个
   - 保险产品: 3 个
   - 评分维度: 4 个
```

### 步骤2: 配置前端

**打开新的命令行窗口**（不要关闭后端的窗口）：

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install
```

> ⏱️ **预计时间**: 2-5分钟（取决于网络速度）

### 步骤3: 启动系统

**启动后端**（在第1个命令行窗口）：

```bash
# 确保在backend目录，并且虚拟环境已激活
python main.py
```

看到以下信息表示后端启动成功：
```
🚀 保险销售智能陪练系统 v1.2.0 启动成功！
📍 API地址: http://127.0.0.1:8000/docs
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**启动前端**（在第2个命令行窗口）：

```bash
# 确保在frontend目录
npm run dev
```

看到以下信息表示前端启动成功：
```
  VITE v5.0.11  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### 步骤4: 开始使用

打开浏览器，访问：**http://localhost:5173**

🎉 **恭喜！系统已成功启动！**

---

## 📖 详细步骤说明

如果您想了解每一步的具体含义，请查看下文：

### 1. 配置后端详解

#### 1.1 创建虚拟环境

```bash
python -m venv venv
```

**作用**: 创建一个独立的Python环境，避免与系统Python冲突

**比喻**: 就像给你的项目盖了一间独立的房子，不会影响其他房间

#### 1.2 激活虚拟环境

**Windows**:
```bash
venv\Scripts\activate
```

**Mac/Linux**:
```bash
source venv/bin/activate
```

**成功标志**: 命令行前面会出现 `(venv)` 标记

#### 1.3 安装依赖

```bash
pip install -r requirements.txt
```

**作用**: 安装项目所需的所有Python库

**时间**: 约2-5分钟

#### 1.4 配置环境变量

编辑 `backend/.env` 文件：

```env
# 必填！填入您的DeepSeek API Key
MODEL_API_KEY=sk-xxxxxxxxxxxxx

# 其他配置可以使用默认值
```

> ⚠️ **重要**: API Key必须正确填写，否则系统无法工作

#### 1.5 初始化数据

```bash
python init_demo_data.py
```

**作用**: 自动创建客户角色、保险产品、评分维度等演示数据

### 2. 配置前端详解

#### 2.1 安装前端依赖

```bash
cd frontend
npm install
```

**作用**: 安装Vue 3、Element Plus等前端库

**时间**: 约2-5分钟

### 3. 启动服务详解

#### 3.1 后端服务

```bash
cd backend
python main.py
```

**作用**: 启动FastAPI后端服务器

**端口**: 8000

**功能**: 提供API接口和WebSocket服务

#### 3.2 前端服务

```bash
cd frontend
npm run dev
```

**作用**: 启动Vite开发服务器

**端口**: 5173

**功能**: 提供用户界面

---

## 🔧 常见问题

### Q1: 提示"python不是内部或外部命令"

**原因**: Python未安装或未添加到系统PATH

**解决**:
1. 重新安装Python，勾选"Add Python to PATH"
2. 或重启电脑后再次尝试

---

### Q2: 提示"node不是内部或外部命令"

**原因**: Node.js未安装

**解决**:
1. 访问 https://nodejs.org/
2. 下载并安装LTS版本
3. 重启命令行窗口

---

### Q3: pip安装失败或很慢

**原因**: 默认pip源在国外，速度慢

**解决**: 使用国内镜像源

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

### Q4: npm安装失败

**原因**: 网络问题或npm源问题

**解决**: 使用淘宝镜像

```bash
npm install --registry=https://registry.npmmirror.com
```

---

### Q5: 启动后提示"API Key未配置"

**原因**: .env文件配置错误

**解决**:
1. 确认已创建 `.env` 文件（不是 `.env.example`）
2. 确认API Key格式正确（以 `sk-` 开头）
3. 确认没有多余的空格或引号

---

### Q6: 前端无法连接后端

**原因**: 后端未启动或端口被占用

**解决**:
1. 确认后端已启动（看到"启动成功"消息）
2. 检查 http://127.0.0.1:8000/docs 是否可访问
3. 如果8000端口被占用，修改 `.env` 中的 `PORT` 值

---

### Q7: 数据库初始化失败

**原因**: 可能是权限问题或目录不存在

**解决**:
```bash
# 手动创建data目录
cd backend
mkdir data

# 重新初始化
python init_demo_data.py
```

---

## 🎬 下一步

启动成功后，您可以：

1. **开始练习** → 选择角色和产品，开始AI对话
2. **查看API文档** → 访问 http://127.0.0.1:8000/docs
3. **阅读文档** → 查看 [README.md](README.md) 和 [DEPLOYMENT.md](DEPLOYMENT.md)
4. **学习Git** → 阅读 [GIT_GUIDE.md](GIT_GUIDE.md)

---

## 📞 获取帮助

如果遇到其他问题：

1. **查看错误日志** → 仔细阅读错误提示
2. **查看文档** → 仔细阅读 README.md 和 DEPLOYMENT.md
3. **提交Issue** → 如果是项目Bug，提交到GitHub Issues

---

## 🛑 停止服务

当您想停止系统时：

**后端**: 在后端命令行窗口按 `Ctrl + C`

**前端**: 在前端命令行窗口按 `Ctrl + C`

---

**祝您使用愉快！** 🎊
