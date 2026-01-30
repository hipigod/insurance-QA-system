# Spring Boot JVM 内存优化与 Docker 环境变量传递实战笔记

## 1. 背景与问题

### 事情从什么情况开始

将保险销售智能陪练系统部署到阿里云服务器后，遇到了两个关联的问题：

1. **WebSocket 连接 1 分钟后自动断开**
   - 用户在进行角色扮演对话时，连接会在空闲约 1 分钟后断开
   - 需要刷新页面才能继续使用，严重影响体验

2. **服务器内存占用过高**
   - 服务器总内存：1.8 GB
   - 后端 Spring Boot 应用占用：约 1000 MB（55%）
   - 剩余可用内存：约 800 MB
   - 影响：无法部署更多项目，且偶发 OOM（内存溢出）

### 核心困扰

虽然两个问题看似独立，但都指向同一个根源：**部署环境的复杂性**。

- WebSocket 超时：系统 Nginx（宝塔）的默认 60 秒超时设置
- 内存占用高：Java 应用的 JVM 默认内存分配策略

---

## 2. 现有做法及局限

### WebSocket 配置的预期与现实

在项目代码中，容器内的 Nginx 配置（`frontend/nginx.conf`）已经考虑到了超时问题：

```nginx
location /ws {
    proxy_pass http://backend:8000;
    proxy_read_timeout 7d;  # ← 看起来已经配置了 7 天超时
}
```

**预期效果**：WebSocket 连接应该能保持 7 天不断开。

**现实情况**：连接在 1 分钟左右还是会断开。

**问题根源**：

服务器上运行着宝塔面板，系统 Nginx 占用了 80 端口。实际的网络请求路径是：

```
用户浏览器
    ↓
宝塔系统 Nginx (80端口) ← 真正的守门人，默认 60 秒超时
    ↓
容器内 Nginx (8081端口) ← 我们配置了 7 天超时
    ↓
后端 Spring Boot (8000端口)
```

**类比**：就像你在公司打电话，前台（系统 Nginx）只让你通话 1 分钟，即使你和朋友（容器）约定聊 7 天也没用，因为前台会先掐线。

---

### JVM 内存占用的现状

Spring Boot 应用的内存占用组成：

```
总内存约 1000 MB：
├─ JVM 堆内存:      ~800 MB (默认使用物理内存的 1/4)
├─ 元空间:          ~128 MB
├─ 代码缓存:        ~50 MB
├─ 线程栈:          ~10 MB
└─ 其他:            ~12 MB
```

**问题**：
- 默认配置下，JVM 会尝试使用最多物理内存的 1/4 作为堆内存
- 对于 1.8 GB 的服务器，堆内存上限约 450 MB，但实际会预留更多
- 应用实际使用的内存可能远低于分配的内存（资源浪费）

---

## 3. 新的解决思路

### WebSocket 问题：双重保障策略

**判断方向**：不能只依赖一层的配置，需要多层防护。

**解决方案**：
1. **修改系统 Nginx 配置**：将超时时间延长到 7 天
2. **添加心跳机制**：每 30 秒发送 ping/pong 消息

**为什么需要两个方案**：
- 仅修改超时配置：依赖各个环节都配置正确，容错性差
- 添加心跳机制：主动保持连接活跃，任何中间层都不会因为没有数据而超时

**类比**：
- **修改超时配置**：像告诉前台"让他们聊久一点"
- **添加心跳机制**：像每隔 30 秒说一声"我还在"，让前台知道通话还在进行

---

### JVM 内存优化：参数限制策略

**判断方向**：不需要让应用占用那么多内存，可以通过 JVM 参数限制。

**解决方案**：
```bash
-Xmx512m                  # 限制最大堆内存为 512 MB
-Xms256m                  # 设置初始堆内存为 256 MB
-XX:MaxMetaspaceSize=128m # 限制元空间大小为 128 MB
```

**预期效果**：
- 从实际占用 ~1000 MB 降到 ~250-300 MB
- 节省约 70% 的内存
- 服务器剩余内存从 ~800 MB 增加到 ~1500 MB

---

## 4. 关键过程：踩坑与修复

### 步骤 1：修复系统 Nginx 配置

**位置**：服务器 `/www/server/panel/vhost/nginx/insurance.conf`

**修改前**：
```nginx
location /ws {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    # ❌ 缺少超时配置
}
```

**修改后**：
```nginx
location /ws {
    proxy_pass http://localhost:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    # ✅ 添加 WebSocket 超时配置
    proxy_connect_timeout 7d;
    proxy_send_timeout 7d;
    proxy_read_timeout 7d;
}
```

---

### 步骤 2：添加 WebSocket 心跳机制

**前端实现**（`frontend/src/views/Dialogue.vue`）：

```javascript
// 1. 定义心跳变量
let heartbeatInterval = null

// 2. 启动心跳函数
const startHeartbeat = () => {
  stopHeartbeat()  // 清除可能存在的旧定时器

  // 每 30 秒发送一次心跳
  heartbeatInterval = setInterval(() => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify({
        type: 'ping',
        timestamp: Date.now()
      }))
      console.log('WebSocket心跳已发送')
    }
  }, 30000)
}

// 3. 在连接成功时启动心跳
websocket.onopen = () => {
  startHeartbeat()
  websocket.send(JSON.stringify({
    type: 'subscribe',
    session_id: sessionId.value
  }))
}

// 4. 在连接关闭时停止心跳
websocket.onclose = () => {
  stopHeartbeat()
}
```

**后端实现**（`backend/ws/DialogueWebSocketHandler.java`）：

```java
// 在消息类型判断中添加 ping 处理
switch (inbound.getType()) {
  case "ping" -> handlePing(session, inbound);  // ← 新增
  // ... 其他类型
}

// 实现心跳处理方法
private void handlePing(WebSocketSession socket, WsMessage inbound) throws Exception {
  WsMessage pong = new WsMessage();
  pong.setType("pong");
  pong.setSessionId(inbound.getSessionId());
  pong.setTimestamp(inbound.getTimestamp());
  socket.sendMessage(new TextMessage(objectMapper.writeValueAsString(pong)));
}
```

---

### 步骤 3：JVM 内存优化（踩坑开始）

#### 第一版：配置 JAVA_OPTS 环境变量

**docker-compose.yml**：
```yaml
services:
  backend:
    environment:
      # JVM 内存优化
      - JAVA_OPTS=-Xmx512m -Xms256m -XX:MaxMetaspaceSize=128m
```

**问题**：环境变量值包含空格，YAML 解析出错。

---

#### 第二版：添加引号（修复 YAML）

**docker-compose.yml**：
```yaml
- JAVA_OPTS="-Xmx512m -Xms256m -XX:MaxMetaspaceSize=128m"
```

**问题**：容器启动后，`env | grep JAVA_OPTS` 仍然查不到环境变量。

---

#### 第三版：修改 Dockerfile 支持 JAVA_OPTS（继续踩坑）

**Dockerfile v1**：
```dockerfile
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

**修改为**：
```dockerfile
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app/app.jar"]
```

**结果**：容器启动失败！

**错误日志**：
```
Error: Could not find or load main class "-Xmx512m
Caused by: java.lang.ClassNotFoundException: "-Xmx512m
```

---

#### 问题根源分析

**为什么失败？**

在 Docker 的 **exec form**（JSON 数组格式）中：
```dockerfile
ENTRYPOINT ["sh", "-c", "java ${JAVA_OPTS} -jar /app/app.jar"]
```

- `${JAVA_OPTS}` **不会被 shell 展开**，而是被当作字面字符串
- 如果 `JAVA_OPTS` 环境变量为空，就变成 `java  -jar /app/app.jar`（两个空格）
- 即使有值，也会被当作字符串的一部分，不会被展开

**类比**：就像你在写代码时，双引号里的变量 `$var` 不会被展开，你需要用 eval 或其他方式。

---

#### 第四版：创建启动脚本（最终方案）

**Dockerfile v2（正确版本）**：
```dockerfile
# 创建启动脚本以支持 JAVA_OPTS 环境变量
RUN echo '#!/bin/sh' > /app/entrypoint.sh && \
    echo 'exec java ${JAVA_OPTS} -jar /app/app.jar' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
```

**为什么这样能工作？**

```
流程：
1. Docker 启动容器，执行 /app/entrypoint.sh
2. 脚本在 shell 中运行
3. Shell 展开环境变量 ${JAVA_OPTS} 为 "-Xmx512m -Xms256m ..."
4. 执行 exec java -Xmx512m -Xms256m ... -jar /app/app.jar
5. Java 进程启动成功！
```

**关键点**：
- ✅ 脚本在 shell 中执行，环境变量会正确展开
- ✅ `exec` 确保Java进程替代脚本进程（PID 1），信号处理正确
- ✅ 不会把参数当作类名

---

## 5. 总结与要点

### 核心结论

1. **WebSocket 问题涉及两个层次**
   - 系统 Nginx 的默认 60 秒超时（第一层）
   - 缺少心跳机制保持连接活跃（第二层）

2. **JVM 内存优化效果显著**
   - 从实际占用 ~1000 MB 降到 ~250 MB
   - 节省了约 75% 的内存
   - 服务器剩余内存从 ~800 MB 增加到 ~1600 MB

3. **Docker 环境变量传递的坑**
   - JSON 数组格式的 ENTRYPOINT 不会展开环境变量
   - 需要创建启动脚本，在 shell 中执行

---

### 可复用的判断原则

#### 原则 1：排查网络问题时，从外到内逐层检查

```
用户浏览器
    ↓
反向代理（Nginx/负载均衡器）  ← 第一层检查
    ↓
容器内 Nginx                   ← 第二层检查
    ↓
后端应用                       ← 第三层检查
```

**实用命令**：
```bash
# 检查外层 Nginx 配置
cat /www/server/panel/vhost/nginx/insurance.conf

# 检查容器内 Nginx 配置
docker exec insurance-frontend cat /etc/nginx/conf.d/default.conf

# 检查后端日志
docker compose logs backend
```

---

#### 原则 2：Docker 环境变量传递的正确方式

| 方式 | 示例 | 是否展开变量 |
|------|------|-------------|
| **exec form（数组）** | `ENTRYPOINT ["java", "-jar", "app.jar"]` | ❌ 不会展开 |
| **shell form（字符串）** | `ENTRYPOINT java -jar app.jar` | ✅ 会展开 |
| **启动脚本** | `ENTRYPOINT ["./script.sh"]` | ✅ 脚本内会展开 |

**推荐**：使用启动脚本的方式，既安全又可靠。

---

#### 原则 3：JVM 内存参数的合理设置

| 应用规模 | 推荐配置 | 说明 |
|---------|---------|------|
| **小型应用** | `-Xmx256m -Xms128m` | 单体应用，用户 < 100 |
| **中型应用** | `-Xmx512m -Xms256m` | 微服务，用户 < 1000 |
| **大型应用** | `-Xmx1g -Xms512m` | 高并发，用户 > 1000 |

**注意**：
- `-Xmx`（最大堆）不应超过物理内存的 50%
- `-Xms`（初始堆）设为 `-Xmx` 的 50% 左右
- 留足够内存给操作系统、元空间、线程栈等

---

#### 原则 4：优化内存前的评估清单

在优化 JVM 内存前，先问自己：

1. **应用实际占用多少内存？**
   ```bash
   docker stats <container-name> --no-stream
   ```

2. **应用负载如何？**
   - 用户并发数
   - 是否有大量缓存
   - 是否有复杂计算

3. **服务器还有多少可用内存？**
   ```bash
   free -h
   ```

4. **优化后有什么风险？**
   - 并发增加时是否会 OOM？
   - GC 频率是否会增加？
   - 响应时间是否会受影响？

---

### 实用命令清单

#### 监控内存使用

```bash
# 查看容器内存占用
docker stats insurance-backend --no-stream

# 查看服务器内存使用
free -h

# 查看进程内存占用（按占用排序）
ps aux --sort=-%mem | head -20
```

#### 验证 JVM 参数

```bash
# 查看环境变量
docker exec <container> env | grep JAVA_OPTS

# 查看进程参数
docker exec <container> ps aux | grep java

# 如果有 JDK，可以查看 JVM 详细参数
docker exec <container> jcmd 1 VM.flags
docker exec <container> jcmd 1 GC.heap_info
```

#### 测试内存压力

```bash
# 查看实时内存使用
watch -n 2 'docker stats insurance-backend --no-stream'

# 查看内存历史
docker stats insurance-backend
```

---

### 避坑指南

1. **不要假设环境是简单的**
   - 服务器上可能已有 Nginx/负载均衡器
   - 可能有多个代理层，每层都可能超时
   - 容器内配置 ≠ 实际生效配置

2. **Docker 构建需要重新**
   - 修改代码后必须重新构建镜像（`--build`）
   - 前端代码在构建时打包，修改后不重建不会生效
   - 注意缓存问题（必要时使用 `--no-cache`）

3. **YAML 语法要小心**
   - 值包含空格时必须用引号
   ```yaml
   # ✅ 正确
   - JAVA_OPTS="-Xmx512m -Xms256m"

   # ❌ 错误
   - JAVA_OPTS=-Xmx512m -Xms256m
   ```

4. **Git 提交要规范**
   - 每个修复应该是一个完整的 commit
   - commit message 要清楚说明问题和解决方案
   - 测试通过后再提交

5. **优化要循序渐进**
   - 先观察当前状态
   - 小步优化，每次只改一个参数
   - 观察效果后再继续
   - 不要一次改太多，否则出问题无法定位

---

### 关键理解

**WebSocket 超时的本质**：

就像打电话：
- **超时配置**：告诉前台"最久让她们聊多久"
- **心跳机制**：每隔一段时间说"我还在"，让前台知道通话还在进行

**为什么要两个方案**：
- 只配置超时：依赖各个环节都配置正确，容错性差
- 只用心跳：增加了网络开销，但更可靠
- **两者结合**：既有长时保障，又有主动保活，是最佳方案

**Docker 环境变量传递的本质**：

```dockerfile
# 方式 1：直接参数（exec form）
ENTRYPOINT ["java", "-jar", "app.jar"]
# → 简单，但无法传递动态参数

# 方式 2：shell 嵌入（exec form + shell）
ENTRYPOINT ["sh", "-c", "java ${VAR} -jar app.jar"]
# → ❌ ${VAR} 不会展开！

# 方式 3：启动脚本（推荐）
ENTRYPOINT ["./script.sh"]
# → ✅ 脚本内 ${VAR} 会正确展开
```

---

## 附录：完整的优化时间线

```
Day 1: WebSocket 1 分钟断连问题
  ├─ 排查：从外到内检查 Nginx 配置
  ├─ 发现：系统 Nginx 默认 60 秒超时
  └─ 解决：配置超时 7 天 + 添加心跳机制
  └─ 结果：WebSocket 问题解决 ✅

Day 2: 决定优化 JVM 内存
  ├─ 修改 docker-compose.yml，添加 JAVA_OPTS
  ├─ 推送代码到服务器
  └─ 发现：环境变量未生效（未加引号）

Day 3: 修复 YAML 引号问题
  ├─ 修改：添加引号
  ├─ 推送代码
  └─ 发现：环境变量还是未生效

Day 4: 深入排查
  ├─ 检查：服务器代码不是最新的
  ├─ 手动拉取代码
  └─ 发现：容器启动失败！

Day 5: 修复 Dockerfile ENTRYPOINT
  ├─ 问题：ENTRYPOINT 不会展开 ${JAVA_OPTS}
  ├─ 尝试：直接写 shell 命令
  ├─ 失败：Java 把参数当作类名
  └─ 解决：创建启动脚本 ✅

Day 6: 最终验证
  ├─ 部署修复后的代码
  ├─ 验证：环境变量存在 ✅
  ├─ 验证：进程有 JVM 参数 ✅
  ├─ 验证：内存占用 ~250 MB ✅
  └─ 结果：优化成功！
```

---

## 结语

这次优化经历展示了：

1. **问题往往不是表面看起来那样**
   - WebSocket 断连不是代码问题，而是配置问题
   - 内存占用高不是应用问题，而是 JVM 默认策略

2. **解决方案需要综合考虑**
   - 不能只依赖一层防护（多层超时配置）
   - 不能只优化一个地方（JVM + 容器 + 应用）

3. **技术细节很重要**
   - Docker 的 exec form vs shell form
   - YAML 的引号规则
   - 环境变量传递机制

4. **耐心和系统性的排查方法**
   - 从外到内逐层检查
   - 小步修改，每次验证
   - 出问题不慌，系统性地排查

**最后的提醒**：优化是一个持续的过程，不是一次性的任务。根据实际使用情况调整参数，才能找到最适合的配置。

---

**相关文档**：
- [Docker部署故障排查实战笔记](./Docker部署故障排查实战笔记.md)
- [WebSocket 1分钟超时断连问题排查与修复](./websocket-1分钟超时断连问题排查与修复.md)
- [远程自动部署使用说明](../REMOTE_DEPLOY.md)
