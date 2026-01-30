# 远程自动部署脚本使用说明

## 📖 简介

`deploy-remote.sh` 是一个自动化部署脚本，可以一键完成以下操作：

1. **SSH连接到服务器**
2. **拉取最新Git代码**
3. **重新构建Docker容器**

---

## 🚀 快速开始

### 第一步：创建配置文件

```bash
# 1. 复制配置文件模板
cp deploy-remote.conf.example deploy-remote.conf

# 2. 编辑配置文件
vi deploy-remote.conf
```

### 第二步：填写配置

```bash
# 最小配置示例
SERVER_HOST="8.138.18.77"              # 你的服务器IP或域名
SERVER_USER="root"                     # SSH用户名
SERVER_PASSWORD=""                     # 如果用SSH密钥，留空即可
PROJECT_PATH="/opt/insurance-QA-system"  # 项目路径
GIT_BRANCH="docker-java"               # Git分支
```

### 第三步：执行部署

```bash
# 一键部署
bash deploy-remote.sh
```

---

## 📝 配置说明

### 必填配置项

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `SERVER_HOST` | 服务器地址（IP或域名） | `8.138.18.77` |
| `SERVER_USER` | SSH用户名 | `root` |
| `PROJECT_PATH` | 项目在服务器上的路径 | `/opt/insurance-QA-system` |
| `GIT_BRANCH` | Git分支名称 | `docker-java` |

### 可选配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `SERVER_PASSWORD` | SSH密码（推荐用密钥） | 空字符串 |
| `SERVER_PORT` | SSH端口 | `22` |

---

## 🔐 SSH认证方式

### 方式1：SSH密钥认证（推荐）

**优势**：安全、无需输入密码

**配置步骤**：

#### 1. 生成SSH密钥对

```bash
# 在本地电脑执行
ssh-keygen -t rsa -b 4096

# 一路回车即可（或设置密码短语）
```

#### 2. 复制公钥到服务器

```bash
# 复制公钥到服务器
ssh-copy-id root@8.138.18.77

# 输入服务器密码后，以后就不需要密码了
```

#### 3. 测试SSH连接

```bash
# 测试是否能免密登录
ssh root@8.138.18.77

# 如果直接登录，说明配置成功
```

#### 4. 配置文件

```bash
# deploy-remote.conf
SERVER_HOST="8.138.18.77"
SERVER_USER="root"
SERVER_PASSWORD=""  # 留空，使用SSH密钥
```

---

### 方式2：密码认证

**不推荐**，因为每次都需要输入密码

如果确实需要使用密码，可以安装 `sshpass`：

#### Mac

```bash
brew install sshpass
```

#### Ubuntu/Debian

```bash
sudo apt install sshpass
```

#### Windows (Git Bash)

```bash
# 下载 sshpass for Windows
# 或使用 WSL
```

然后配置文件：

```bash
# deploy-remote.conf
SERVER_HOST="8.138.18.77"
SERVER_USER="root"
SERVER_PASSWORD="your_password_here"  # 不安全，但可以用
```

---

## 📋 脚本执行流程

```
1. 加载配置文件 (deploy-remote.conf)
   ↓
2. 测试SSH连接
   ↓
3. 在服务器上执行：
   ├─ cd $PROJECT_PATH
   ├─ git pull origin $GIT_BRANCH
   ├─ docker compose down
   └─ docker compose up --build -d
   ↓
4. 验证部署结果
   ├─ 查看容器状态
   ├─ 查看内存占用
   └─ 验证环境变量
   ↓
5. 显示部署信息
```

---

## ✅ 验证部署

部署完成后，脚本会自动验证以下内容：

### 1. 容器状态

```bash
docker compose ps
```

**预期输出**：
```
insurance-backend   Up (healthy)
insurance-frontend  Up (healthy)
```

### 2. 内存占用

```bash
docker stats insurance-backend --no-stream
```

**预期输出**：
```
MEM USAGE: ~200-300 MB
```

### 3. JVM参数

```bash
docker exec insurance-backend env | grep JAVA_OPTS
```

**预期输出**：
```
JAVA_OPTS=-Xmx512m -Xms256m -XX:MaxMetaspaceSize=128m
```

### 4. 进程参数

```bash
docker exec insurance-backend ps aux | grep java
```

**预期输出**：
```
java -Xmx512m -Xms256m -XX:MaxMetaspaceSize=128m -jar /app/app.jar
```

---

## 🎯 使用示例

### 示例1：首次部署

```bash
# 1. 创建配置文件
cp deploy-remote.conf.example deploy-remote.conf

# 2. 编辑配置
vi deploy-remote.conf

# 3. 执行部署
bash deploy-remote.sh
```

### 示例2：更新代码后重新部署

```bash
# 修改代码并推送到Git后，直接执行
bash deploy-remote.sh
```

### 示例3：使用不同的分支

```bash
# 修改配置文件
vi deploy-remote.conf

# 改为其他分支
GIT_BRANCH="main"

# 执行部署
bash deploy-remote.sh
```

---

## 🔧 故障排查

### 问题1：SSH连接失败

**错误信息**：
```
[ERROR] SSH连接失败
```

**解决方法**：

1. 检查服务器地址是否正确
   ```bash
   ping 8.138.18.77
   ```

2. 检查SSH密钥是否配置
   ```bash
   ssh root@8.138.18.77
   ```

3. 如果使用密码，确保已安装 sshpass

---

### 问题2：Git拉取失败

**错误信息**：
```
error: cannot pull with rebase
```

**解决方法**：

```bash
# SSH到服务器手动解决
ssh root@8.138.18.77
cd /opt/insurance-QA-system
git status
# 根据提示解决冲突或暂存本地修改
```

---

### 问题3：容器构建失败

**错误信息**：
```
ERROR: for insurance-backend  failed to build
```

**解决方法**：

```bash
# 查看详细错误日志
ssh root@8.138.18.77
cd /opt/insurance-QA-system
docker compose logs backend
```

---

## 📊 完整示例

### 配置文件示例

```bash
# deploy-remote.conf
SERVER_HOST="8.138.18.77"
SERVER_USER="root"
SERVER_PASSWORD=""
PROJECT_PATH="/opt/insurance-QA-system"
GIT_BRANCH="docker-java"
```

### 执行输出示例

```bash
$ bash deploy-remote.sh

========================================
  远程自动部署脚本
========================================

[INFO] 配置文件加载成功
[INFO] 服务器: root@8.138.18.77
[INFO] 项目路径: /opt/insurance-QA-system
[INFO] Git分支: docker-java

=====> 步骤1：SSH连接到服务器

[SUCCESS] SSH连接测试成功

=====> 步骤2：拉取最新代码

[INFO] 进入项目目录: /opt/insurance-QA-system
[INFO] 拉取分支: docker-java
[SUCCESS] 代码拉取成功

=====> 步骤3：重新构建并启动容器

[SUCCESS] 容器重新构建成功

=====> 验证部署结果

[SUCCESS] 部署完成！

========================================
    远程部署成功完成！
========================================
```

---

## 💡 最佳实践

1. **使用SSH密钥认证** - 安全且便捷
2. **配置文件不要提交到Git** - 已在 .gitignore 中
3. **定期更新代码** - 保持项目最新
4. **部署后验证功能** - 确保一切正常

---

## 📚 相关文档

- [Docker部署故障排查实战笔记](./problemsolve/Docker部署故障排查实战笔记.md)
- [WebSocket超时问题排查](./problemsolve/websocket-1分钟超时断连问题排查与修复.md)

---

## 🆘 需要帮助？

如果遇到问题：

1. 查看本文档的故障排查部分
2. 查看项目其他文档
3. 检查服务器日志：`docker compose logs backend`

---

**祝你部署顺利！** 🚀
