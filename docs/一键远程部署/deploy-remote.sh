#!/bin/bash

################################################################################
# 自动化远程部署脚本
# 功能：SSH连接服务器，拉取代码，重新构建Docker容器
################################################################################

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "\n${GREEN}=====> $1${NC}\n"
}

# 加载配置文件
load_config() {
    if [ ! -f "deploy-remote.conf" ]; then
        print_error "配置文件 deploy-remote.conf 不存在"
        print_info "请先创建配置文件："
        print_info "  1. cp deploy-remote.conf.example deploy-remote.conf"
        print_info "  2. 编辑 deploy-remote.conf 填写配置"
        exit 1
    fi

    # 读取配置文件
    source deploy-remote.conf

    # 验证必填配置
    if [ -z "$SERVER_HOST" ]; then
        print_error "配置文件中未设置 SERVER_HOST"
        exit 1
    fi

    if [ -z "$SERVER_USER" ]; then
        print_error "配置文件中未设置 SERVER_USER"
        exit 1
    fi

    if [ -z "$PROJECT_PATH" ]; then
        print_error "配置文件中未设置 PROJECT_PATH"
        exit 1
    fi

    if [ -z "$GIT_BRANCH" ]; then
        print_error "配置文件中未设置 GIT_BRANCH"
        exit 1
    fi

    print_success "配置文件加载成功"
    print_info "服务器: $SERVER_USER@$SERVER_HOST"
    print_info "项目路径: $PROJECT_PATH"
    print_info "Git分支: $GIT_BRANCH"
}

# 步骤1：SSH连接到服务器
step1_connect_server() {
    print_step "步骤1：SSH连接到服务器"

    print_info "正在连接服务器: $SERVER_USER@$SERVER_HOST"

    # 测试SSH连接
    if ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no \
        "$SERVER_USER@$SERVER_HOST" "echo 'SSH连接成功'" > /dev/null 2>&1; then
        print_success "SSH连接测试成功"
    else
        print_error "SSH连接失败"
        print_info "请检查："
        print_info "  1. 服务器地址是否正确: $SERVER_HOST"
        print_info "  2. SSH密钥是否已配置（或使用密码）"
        print_info "  3. 网络是否通畅"
        exit 1
    fi
}

# 步骤2：拉取最新代码
step2_pull_code() {
    print_step "步骤2：拉取最新代码"

    print_info "进入项目目录: $PROJECT_PATH"
    print_info "拉取分支: $GIT_BRANCH"

    # 在远程服务器上执行命令
    ssh "$SERVER_USER@$SERVER_HOST" bash << EOF
        set -e

        # 进入项目目录
        cd $PROJECT_PATH

        # 检查是否是Git仓库
        if [ ! -d ".git" ]; then
            echo "错误：不是一个Git仓库"
            exit 1
        fi

        # 查看当前分支
        CURRENT_BRANCH=\$(git branch --show-current)
        echo "当前分支: \$CURRENT_BRANCH"

        # 拉取最新代码
        echo "正在拉取最新代码..."
        git pull origin $GIT_BRANCH

        # 显示最新提交
        echo "最新提交："
        git log -1 --oneline

        exit 0
EOF

    if [ $? -eq 0 ]; then
        print_success "代码拉取成功"
    else
        print_error "代码拉取失败"
        exit 1
    fi
}

# 步骤3：重新构建并启动容器
step3_rebuild_container() {
    print_step "步骤3：重新构建并启动容器"

    ssh "$SERVER_USER@$SERVER_HOST" bash << EOF
        set -e
        cd $PROJECT_PATH

        echo "停止旧容器..."
        docker compose down

        echo "重新构建并启动容器..."
        docker compose up --build -d

        echo "等待容器启动..."
        sleep 10

        echo "查看容器状态..."
        docker compose ps

        exit 0
EOF

    if [ $? -eq 0 ]; then
        print_success "容器重新构建成功"
    else
        print_error "容器重新构建失败"
        exit 1
    fi
}

# 验证部署结果
verify_deployment() {
    print_step "验证部署结果"

    ssh "$SERVER_USER@$SERVER_HOST" bash << EOF
        set -e
        cd $PROJECT_PATH

        echo "查看后端日志（最近20行）："
        docker compose logs backend --tail 20

        echo ""
        echo "查看内存占用："
        docker stats insurance-backend --no-stream

        echo ""
        echo "验证环境变量："
        docker exec insurance-backend env | grep JAVA_OPTS || echo "环境变量未找到"

        exit 0
EOF
}

# 显示部署信息
show_deployment_info() {
    print_step "部署完成"

    cat << EOF

${GREEN}========================================
    远程部署成功完成！
========================================${NC}

${GREEN}部署信息:${NC}
  服务器:    $SERVER_USER@$SERVER_HOST
  项目路径:  $PROJECT_PATH
  Git分支:   $GIT_BRANCH

${GREEN}验证命令:${NC}
  # SSH连接到服务器
  ssh $SERVER_USER@$SERVER_HOST

  # 进入项目目录
  cd $PROJECT_PATH

  # 查看容器状态
  docker compose ps

  # 查看后端日志
  docker compose logs -f backend

  # 查看内存占用
  docker stats insurance-backend

${GREEN}浏览器访问:${NC}
  http://insurance.hipigod.top/

${GREEN}========================================${NC}

EOF
}

# 主函数
main() {
    echo -e "${GREEN}"
    cat << "EOF"
========================================
  远程自动部署脚本
========================================
EOF
    echo -e "${NC}"

    # 执行部署步骤
    load_config
    step1_connect_server
    step2_pull_code
    step3_rebuild_container
    verify_deployment
    show_deployment_info
}

# 捕获错误
trap 'print_error "部署失败，请检查错误信息"; exit 1' ERR

# 运行主函数
main
