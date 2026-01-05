@echo off
REM 重启后端服务器
echo ========================================
echo 重启后端服务器
echo ========================================
echo.

echo [1/2] 停止现有的后端服务...
taskkill /f /fi "WINDOWTITLE eq 后端服务*" >nul 2>&1
if errorlevel 1 (
    echo 没有找到运行中的后端服务
) else (
    echo 后端服务已停止
)

echo.
echo [2/2] 启动新的后端服务...
start "后端服务" cmd /k "cd backend && python main.py"

echo.
echo ========================================
echo 后端服务已重启!
echo.
echo API 文档: http://127.0.0.1:8000/docs
echo Models API: http://127.0.0.1:8000/api/models/
echo ========================================
echo.

REM 等待服务启动
timeout /t 3 /nobreak >nul

REM 测试服务
echo 测试服务连接...
python backend\test_endpoint.py

pause
