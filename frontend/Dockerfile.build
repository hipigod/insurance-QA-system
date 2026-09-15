# 构建阶段 - 使用Node.js 18（解决crypto兼容性问题）
FROM node:18-alpine as builder

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 安装依赖（包括开发依赖，因为构建需要vite）
RUN npm ci

# 复制项目文件
COPY . .

# 设置权限
RUN chmod +x node_modules/.bin/* && \
    chmod -R 755 /app

# 设置环境变量
ENV NODE_ENV=production

# 构建应用
RUN npm run build

# 生产阶段 - 使用Nginx
FROM nginx:alpine

# 安装curl（用于健康检查）
RUN apk add --no-cache curl

# 复制构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 创建nginx运行时目录
RUN mkdir -p /var/cache/nginx/client_temp \
    /var/cache/nginx/proxy_temp \
    /var/cache/nginx/fastcgi_temp \
    /var/cache/nginx/uwsgi_temp \
    /var/cache/nginx/scgi_temp \
    /var/run \
    && chmod -R 755 /var/cache/nginx /var/run

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost/ || exit 1

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]
