# 📚 文档中心

欢迎来到保险销售智能陪练系统的文档中心!

## 📂 目录结构

```
docs/
├── guides/          # 使用指南和开发文档
├── reports/         # 测试报告和Bug修复报告
└── prd/            # 产品需求和测试计划
```

---

## 📖 使用指南 (guides/)

### 用户文档
- [快速开始指南](guides/QUICKSTART.md) - 系统快速入门
- [部署运行指南](guides/DEPLOY_RUN.md) - 部署和运行说明
- [Web服务器部署](guides/Web服务器部署.md) - Web服务器部署文档
- [模型配置指南](guides/MODEL_CONFIG_GUIDE.md) - AI模型配置说明

### Docker部署
- [Docker部署完整指南](DOCKER_DEPLOYMENT.md) - Docker容器化部署完整指南
- [Docker项目结构说明](DOCKER_PROJECT_STRUCTURE.md) - Docker化项目结构详解

### 开发文档
- [Git工作流指南](guides/GIT_GUIDE.md) - Git版本控制规范
- [启动说明](guides/启动说明.md) - 应用启动说明
- [预设数据说明](guides/预设数据说明.md) - 预设数据配置说明

---

## 📊 测试报告 (reports/)

### Bug修复报告
- [BUG-003: 评分报告为空问题修复](reports/BUG-评分报告为空-修复报告.md) - 2025-12-31
- [Bug修复总结](reports/Bug修复总结.md) - 多个Bug修复汇总
- [Bug修复完成报告](reports/Bug修复完成报告.md) - Bug修复状态报告

### 测试总结
- [测试总结报告 V2.1 (最终版)](reports/测试总结报告-V2.1-最终版.md) - 完整测试结果
- [测试报告](reports/测试报告.md) - 功能测试报告
- [TEST_SUMMARY](reports/TEST_SUMMARY.md) - 测试总结

### 诊断报告
- [DIAGNOSIS_REPORT](reports/DIAGNOSIS_REPORT.md) - 模型API路由问题诊断
- [DIAGNOSTIC_TOOLS_INDEX](reports/DIAGNOSTIC_TOOLS_INDEX.md) - 诊断工具索引
- [SOLUTION_SUMMARY](reports/SOLUTION_SUMMARY.md) - 解决方案总结

### 部署报告
- [部署总结](reports/部署总结.md) - 系统部署总结

---

## 📋 产品需求 (prd/)

### 需求文档
- [产品需求文档 V1.2](prd/PRD-保险销售智能陪练系统demo-V1.2.md) - 完整产品需求文档
- [测试计划](prd/TEST_PLAN.md) - 完整测试计划 V2.0 (25个测试用例)

---

## 🔧 开发脚本 (scripts/)

### 数据初始化脚本
- `add_model_config.py` - 添加模型配置
- `add_preset_data.py` - 添加预设数据
- `init_demo_data.py` - 初始化演示数据
- `init_preset_data.py` - 初始化预设数据

### 诊断和测试脚本
- `check_routes_detail.py` - 检查路由详细信息
- `check_running_server.py` - 检查运行中的服务器
- `debug_routes.py` - 调试路由问题
- `runtime_test.py` - 运行时测试
- `simple_route_check.py` - 简单路由检查
- `system_test.py` - 系统测试
- `test_endpoint.py` - 端点测试
- `test_server_start.py` - 服务器启动测试
- `verify_fix.py` - 验证修复
- `verify_old_code.py` - 验证旧代码

---

## 🎯 快速导航

### 我想了解...
- **如何使用系统?** → 查看 [快速开始指南](guides/快速开始.md)
- **如何搭建开发环境?** → 查看 [开发环境搭建](guides/开发环境搭建.md)
- **有哪些Bug已修复?** → 查看 [Bug修复总结](reports/Bug修复总结.md)
- **最新的测试结果?** → 查看 [测试总结报告 V2.1](reports/测试总结报告-V2.1-最终版.md)
- **系统架构设计?** → 查看 [系统架构设计](guides/系统架构设计.md)

### 我想查找...
- **特定Bug的修复** → 浏览 [reports/](reports/) 目录
- **测试用例** → 查看 [TEST_PLAN](prd/TEST_PLAN.md)
- **诊断工具** → 浏览 [scripts/](../scripts/) 目录

---

## 📝 文档规范

### 文档分类
| 类型 | 目录 | 说明 |
|------|------|------|
| 用户指南 | `guides/` | 面向用户的使用说明 |
| 开发文档 | `guides/` | 面向开发者的技术文档 |
| 测试报告 | `reports/` | 功能测试、Bug修复报告 |
| 诊断报告 | `reports/` | 问题诊断和分析报告 |
| 需求文档 | `prd/` | 产品需求和测试计划 |

### 命名规范
- 测试报告: `TEST_REPORT_YYYY-MM-DD.md`
- Bug修复: `BUG-问题简述-修复报告.md`
- 总结报告: `测试总结报告-VX.X.md`
- 用户指南: `功能名称.md`

---

## 🔄 文档更新记录

| 日期 | 更新内容 | 负责人 |
|------|---------|--------|
| 2026-01-05 | 清理冗余文档，删除9个过时文档 | Claude Code |
| 2025-12-31 | 创建文档中心,整理所有文档 | Claude Code |
| 2025-12-31 | 添加BUG-003评分报告修复报告 | Claude Code |

---

## 📞 联系方式

如有文档相关问题,请通过以下方式联系:
- 提交 Issue
- 发送邮件
- 在线咨询

---

**最后更新**: 2025-12-31
**文档版本**: V1.0
**维护人员**: Claude Code AI Assistant
