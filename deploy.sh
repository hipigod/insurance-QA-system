#!/bin/bash

# ====================================
# 保险销售智能陪练系统 - Docker部署脚本
# ====================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查Docker是否安装
check_docker() {
    print_info "检查Docker环境..."

    if ! command -v docker &> /dev/null; then
        print_error "Docker未安装，请先安装Docker"
        echo "访问 https://docs.docker.com/get-docker/ 获取安装指南"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose未安装，请先安装Docker Compose"
        echo "访问 https://docs.docker.com/compose/install/ 获取安装指南"
        exit 1
    fi

    print_info "Docker环境检查通过 ✓"
}

# 检查环境变量文件
check_env_file() {
    print_info "检查环境变量配置..."

    if [ ! -f .env ]; then
        print_warn ".env文件不存在，从模板创建..."
        if [ -f .env.example ]; then
            cp .env.example .env
            print_info "已创建.env文件"
            print_warn "请编辑.env文件，填入MODEL_API_KEY"
            print_info "编辑命令: nano .env 或 vim .env"
            read -p "是否现在编辑.env文件? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                ${EDITOR:-nano} .env
            fi
        else
            print_error ".env.example文件不存在"
            exit 1
        fi
    else
        print_info ".env文件已存在 ✓"
    fi

    # 检查API_KEY是否已配置
    if grep -q "your_api_key_here" .env 2>/dev/null; then
        print_error "请先配置.env文件中的MODEL_API_KEY"
        exit 1
    fi
}

# 创建必要的目录
create_directories() {
    print_info "创建必要的目录..."

    mkdir -p backend/data
    mkdir -p backups

    print_info "目录创建完成 ✓"
}

# 构建镜像
build_images() {
    print_info "开始构建Docker镜像..."
    print_info "这可能需要几分钟时间，请耐心等待..."

    docker-compose build --no-cache

    print_info "镜像构建完成 ✓"
}

# 启动服务
start_services() {
    print_info "启动服务..."

    docker-compose up -d

    print_info "服务启动完成 ✓"
}

# 等待服务就绪
wait_for_services() {
    print_info "等待服务就绪..."

    # 等待后端健康检查
    print_info "等待后端服务..."
    max_attempts=30
    attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if docker-compose exec -T backend python -c "import requests; requests.get('http://localhost:8000/health')" 2>/dev/null; then
            print_info "后端服务就绪 ✓"
            break
        fi
        attempt=$((attempt + 1))
        sleep 2
        echo -n "."
    done

    if [ $attempt -eq $max_attempts ]; then
        print_warn "后端服务可能未完全启动，请检查日志"
    fi

    # 等待前端健康检查
    print_info "等待前端服务..."
    sleep 5

    print_info "服务就绪检查完成 ✓"
}

# 显示部署信息
show_deployment_info() {
    echo ""
    echo "=========================================="
    print_info "部署完成！"
    echo "=========================================="
    echo ""
    echo "🌐 访问地址："
    echo "   前端: http://localhost"
    echo "   后端: http://localhost:8000"
    echo "   API文档: http://localhost:8000/docs"
    echo ""
    echo "📊 容器状态："
    docker-compose ps
    echo ""
    echo "📝 常用命令："
    echo "   查看日志: docker-compose logs -f"
    echo "   停止服务: docker-compose stop"
    echo "   重启服务: docker-compose restart"
    echo "   删除容器: docker-compose down"
    echo ""
    echo "📚 更多信息请查看: DOCKER_DEPLOYMENT.md"
    echo "=========================================="
}

# 主流程
main() {
    echo ""
    echo "=========================================="
    echo "  保险销售智能陪练系统 - Docker部署"
    echo "=========================================="
    echo ""

    # 检查环境
    check_docker

    # 检查配置
    check_env_file

    # 创建目录
    create_directories

    # 构建镜像
    build_images

    # 启动服务
    start_services

    # 等待就绪
    wait_for_services

    # 显示信息
    show_deployment_info
}

# 执行主流程
main
