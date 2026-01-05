@echo off
REM ====================================
REM 保险销售智能陪练系统 - Docker部署脚本 (Windows)
REM ====================================

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo   保险销售智能陪练系统 - Docker部署
echo ==========================================
echo.

REM 检查Docker
echo [INFO] 检查Docker环境...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker未安装，请先安装Docker Desktop
    echo 访问 https://docs.docker.com/desktop/install/windows-install/ 获取安装指南
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose未安装
    pause
    exit /b 1
)

echo [INFO] Docker环境检查通过

REM 检查环境变量
echo [INFO] 检查环境变量配置...
if not exist .env (
    echo [WARN] .env文件不存在，从模板创建...
    if exist .env.example (
        copy .env.example .env >nul
        echo [INFO] 已创建.env文件
        echo [WARN] 请编辑.env文件，填入MODEL_API_KEY
        echo.
        set /p EDITNOW="是否现在编辑.env文件? (y/n): "
        if /i "!EDITNOW!"=="y" (
            notepad .env
        )
    ) else (
        echo [ERROR] .env.example文件不存在
        pause
        exit /b 1
    )
) else (
    echo [INFO] .env文件已存在
)

REM 检查API_KEY
findstr /C:"your_api_key_here" .env >nul 2>&1
if not errorlevel 1 (
    echo [ERROR] 请先配置.env文件中的MODEL_API_KEY
    pause
    exit /b 1
)

REM 创建目录
echo [INFO] 创建必要的目录...
if not exist backend\data mkdir backend\data
if not exist backups mkdir backups
echo [INFO] 目录创建完成

REM 构建镜像
echo [INFO] 开始构建Docker镜像...
echo [INFO] 这可能需要几分钟时间，请耐心等待...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] 镜像构建失败
    pause
    exit /b 1
)
echo [INFO] 镜像构建完成

REM 启动服务
echo [INFO] 启动服务...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] 服务启动失败
    pause
    exit /b 1
)
echo [INFO] 服务启动完成

REM 等待服务就绪
echo [INFO] 等待服务就绪...
timeout /t 10 /nobreak >nul

echo.
echo ==========================================
echo [INFO] 部署完成！
echo ==========================================
echo.
echo 🌐 访问地址：
echo    前端: http://localhost
echo    后端: http://localhost:8000
echo    API文档: http://localhost:8000/docs
echo.
echo 📊 容器状态：
docker-compose ps
echo.
echo 📝 常用命令：
echo    查看日志: docker-compose logs -f
echo    停止服务: docker-compose stop
echo    重启服务: docker-compose restart
echo    删除容器: docker-compose down
echo.
echo 📚 更多信息请查看: DOCKER_DEPLOYMENT.md
echo ==========================================
echo.
pause
