@echo off
REM 一键启动脚本 - Windows

echo ========================================
echo 保险销售智能陪练系统 - 快速启动
echo ========================================
echo.

REM 检查依赖是否安装
echo [1/4] 检查依赖...
python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo 后端依赖未安装，正在安装...
    cd backend
    pip install -r requirements.txt --prefer-binary
    cd ..
)

echo.
echo [2/4] 初始化演示数据...
if not exist "backend\data\insurance_practice.db" (
    python init_demo_data.py
) else (
    echo 数据库已存在，跳过初始化
)

echo.
echo [3/4] 启动后端服务...
start "后端服务" cmd /k "cd backend && python main.py"

REM 等待后端启动
timeout /t 3 /nobreak >nul

echo.
echo [4/4] 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo 系统启动中...
echo.
echo 后端服务: http://127.0.0.1:8000/docs
echo 前端服务: http://localhost:5173
echo.
echo 请等待几秒后访问前端地址
echo ========================================
echo.

REM 自动打开浏览器
timeout /t 5 /nobreak >nul
start http://localhost:5173
