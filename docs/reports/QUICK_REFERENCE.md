# 快速参考 - /api/models/ 404 问题

## 问题
访问 `http://127.0.0.1:8000/api/models/` 返回 404

## 原因
服务器使用旧代码,需要重启

## 解决方法

### 方式 1: 一键重启(推荐)
```bash
cd "e:\codeproject\Insurance Q&A System"
restart_backend.bat
```

### 方式 2: 手动重启
1. 停止后端服务窗口(Ctrl+C)
2. 重新运行: `cd backend && python main.py`

## 验证
```bash
cd backend
python verify_fix.py
```

或访问: http://127.0.0.1:8000/api/models/

## 已改进
- ✅ 启用自动重载(修改代码后自动生效)
- ✅ 创建重启脚本
- ✅ 创建诊断工具

## 文件位置
- 重启脚本: `restart_backend.bat`
- 验证脚本: `backend/verify_fix.py`
- 详细报告: `backend/SOLUTION_SUMMARY.md`
