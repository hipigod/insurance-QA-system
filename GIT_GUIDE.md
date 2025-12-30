# Git版本管理指南

> 面向非技术人员的Git操作教程

---

## 📚 目录

1. [Git是什么](#git是什么)
2. [基本概念](#基本概念)
3. [常用命令](#常用命令)
4. [工作流程](#工作流程)
5. [常见场景](#常见场景)
6. [最佳实践](#最佳实践)

---

## Git是什么

Git是一个**版本控制系统**，就像游戏的"存档"功能：
- 💾 随时保存项目状态
- 🔄 可以回退到任意版本
- 👥 多人协作不冲突
- 📊 查看每次修改了什么

---

## 基本概念

### 三个区域

```
工作区     →   暂存区    →   本地仓库   →   远程仓库
(你的代码)   (准备提交)   (本地版本)    (GitHub/Gitee)
   ↑           ↑           ↑             ↑
  编辑       add       commit        push
```

**简单理解**：
- **工作区**：你正在编辑的文件
- **暂存区**：准备提交的文件（购物车）
- **本地仓库**：已经保存的版本（订单）
- **远程仓库**：云端备份（快递）

---

## 常用命令

### 🔍 查看状态

```bash
git status
```

**作用**：查看当前有哪些文件被修改了

**示例输出**：
```
On branch master
Changes not staged for commit:
  modified:   backend/main.py
```

**解读**：`backend/main.py` 这个文件被修改了，但还没提交

---

### ➕ 添加文件到暂存区

```bash
# 添加单个文件
git add backend/main.py

# 添加所有修改的文件
git add .

# 添加某个目录下的所有文件
git add backend/
```

**作用**：将修改的文件标记为"准备提交"

**比喻**：把商品放入购物车

---

### ✅ 提交到本地仓库

```bash
git commit -m "描述你做了什么"
```

**作用**：将暂存区的文件保存到本地仓库

**比喻**：结算购物车，生成订单

**示例**：
```bash
git commit -m "修复了评分功能的bug"
```

**注意事项**：
- 提交信息要清晰描述修改内容
- 中文可以，但推荐用英文
- 不要用"update"、"fix"这种模糊的描述

---

### 📤 推送到远程仓库

```bash
git push
```

**作用**：将本地提交上传到GitHub/Gitee

**比喻**：把订单发货出去

**首次推送需要设置上游分支**：
```bash
git push -u origin master
```

---

### 📥 从远程仓库拉取

```bash
git pull
```

**作用**：从远程仓库下载最新的修改

**使用场景**：
- 别人推送了新代码
- 你在另一台电脑上工作过

---

### 🔄 查看提交历史

```bash
git log
```

**作用**：查看所有的提交记录

**更友好的查看方式**：
```bash
git log --oneline --graph --all
```

**示例输出**：
```
* c9dabe2 feat: 初始化项目
```

---

## 工作流程

### 日常开发流程

```bash
# 1. 开始工作前，先拉取最新代码
git pull

# 2. 编辑代码...
# (使用VSCode编辑文件)

# 3. 查看修改了什么
git status

# 4. 添加修改的文件
git add .

# 5. 提交修改
git commit -m "feat: 添加了用户登录功能"

# 6. 推送到远程
git push
```

---

## 常见场景

### 场景1: 提交后发现写错了

**问题**：提交信息写错了，或者漏了一个文件

**解决方案**：

```bash
# 如果还没push，修改最后一次提交
git add漏掉的文件
git commit --amend -m "正确的提交信息"
```

---

### 场景2: 想撤销某个文件的修改

```bash
# 撤销工作区的修改（恢复到最后一次提交的状态）
git checkout backend/main.py

# 或使用新命令
git restore backend/main.py
```

⚠️ **警告**：这个操作会**丢失**你的修改，不可恢复！

---

### 场景3: 想查看某个文件修改了什么

```bash
git diff backend/main.py
```

**作用**：对比工作区和暂存区的差异

---

### 场景4: 想回到某个历史版本

```bash
# 1. 先查看历史记录
git log --oneline

# 2. 回到指定版本（创建新分支）
git checkout <commit-hash>

# 或
git switch -c new-branch <commit-hash>
```

⚠️ **注意**：不要直接回到历史版本继续开发，应该创建新分支

---

## 最佳实践

### ✅ 好的提交信息

```bash
# ✅ 清晰描述
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复评分计算错误"
git commit -m "docs: 更新README文档"

# ❌ 模糊描述
git commit -m "update"
git commit -m "fix"
git commit -m "修改了一些东西"
```

### 提交信息规范

推荐使用**约定式提交**格式：

```
<类型>: <简短描述>

[可选的详细描述]
```

**类型**：
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档修改
- `style`: 代码格式（不影响功能）
- `refactor`: 重构代码
- `test`: 添加测试
- `chore`: 构建/工具修改

**示例**：
```bash
git commit -m "feat: 添加WebSocket实时对话功能"
git commit -m "fix: 修复AI评分计算错误"
git commit -m "docs: 更新部署文档"
```

---

### 📏 提交频率

- ✅ **频繁提交**：每完成一个小功能就提交
- ❌ **不要堆积**：不要攒了几十个修改才一次性提交

**建议**：
- 完成一个功能点 → 提交一次
- 修复一个bug → 提交一次
- 写完文档 → 提交一次

---

### 🚫 不要提交的东西

这些文件已经在 `.gitignore` 中配置，Git会自动忽略：

```
# 敏感信息
.env                # API密钥配置
*.key              # 密钥文件

# 临时文件
__pycache__/       # Python缓存
node_modules/      # Node依赖
*.log              # 日志文件

# 系统文件
.DS_Store          # Mac系统文件
Thumbs.db          # Windows缩略图
```

---

### 🔒 提交前检查清单

在 `git push` 之前，确保：

- [ ] 测试代码能正常运行
- [ ] 没有提交敏感信息（密码、密钥）
- [ ] 提交信息清晰明确
- [ ] 没有将不该提交的文件加入（如node_modules）
- [ ] 先 `git pull` 一下，确保代码是最新的

---

## 与远程仓库协作

### 首次关联远程仓库

```bash
# 添加远程仓库地址
git remote add origin https://github.com/username/repo.git

# 查看远程仓库
git remote -v
```

### 推送到远程

```bash
# 首次推送（设置上游分支）
git push -u origin master

# 后续推送
git push
```

### 从远程拉取

```bash
# 拉取并合并
git pull

# 或分两步
git fetch
git merge origin/master
```

---

## 常见问题解决

### Q1: push失败，提示"updates were rejected"

**原因**：远程仓库有本地没有的更新

**解决**：
```bash
# 先拉取
git pull

# 如果有冲突，解决冲突后
git add .
git commit
git push
```

---

### Q2: 提交时提示"nothing to commit"

**原因**：没有修改，或者修改已经提交了

**解决**：
```bash
# 查看状态
git status
```

---

### Q3: 忘记推送，在另一台电脑上工作了

**场景**：
- 电脑A：commit了，但没push
- 电脑B：也在工作，然后push了
- 电脑A：现在想push

**解决**：
```bash
# 在电脑A上
git pull  # 先拉取B的修改
# 手动解决冲突
git add .
git commit
git push
```

---

## 推荐工具

### 🖥️ 图形界面工具（更适合新手）

1. **GitHub Desktop**（Windows/Mac）
   - 免费，官方出品
   - 界面简洁，易于上手

2. **SourceTree**（Windows/Mac）
   - 功能强大
   - 可视化分支管理

3. **VSCode Git集成**
   - 无需离开编辑器
   - 可视化操作

### 📱 命令行工具（推荐熟练后使用）

- **Git Bash**（Windows）
- **Terminal**（Mac/Linux）

---

## 进阶技巧

### 查看某次提交的详细修改

```bash
git show <commit-hash>
```

### 暂存当前工作（切换分支前）

```bash
git stash
# 做其他事情...
git stash pop  # 恢复之前的工作
```

### 撤销最后一次提交（如果还没push）

```bash
git reset --soft HEAD~1
# 修改会保留在工作区
```

---

## 需要帮助？

- 📖 [Git官方文档](https://git-scm.com/doc)
- 🎥 [Git教程视频](https://learngitbranching.js.org/)
- 💬 向团队技术负责人求助

---

**记住**：Git是来帮助你的，不要害怕它！多练习就能掌握。 💪
