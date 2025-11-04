# ValueCell Docker 运行指南

本指南将帮助您使用Docker快速部署和运行ValueCell项目。

## 前提条件

- 安装 [Docker](https://docs.docker.com/get-docker/)
- 安装 [Docker Compose](https://docs.docker.com/compose/install/)（可选，但推荐）

## 快速开始

### 方法1：使用 Docker Compose（推荐）

1. **配置环境变量**

```bash
cp .env.example .env
```

编辑 `.env` 文件，添加您的API密钥（至少需要配置一个LLM提供商）：

```bash
# OpenRouter（推荐）
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx

# 或者 SiliconFlow
SILICONFLOW_API_KEY=sk-xxxxxxxxxxxxx

# 或者 Google Gemini
GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxx
```

2. **启动服务**

```bash
docker compose up -d
```

### 方法2：使用 Docker 命令

1. **构建镜像**（如果尚未构建）

```bash
docker build -t valuecell .
```

2. **配置环境变量**

```bash
cp .env.example .env
```

3. **运行容器**

```bash
docker run -d \
  --name valuecell \
  -p 1420:1420 \
  -p 8002:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/lancedb:/app/lancedb \
  -v $(pwd)/valuecell.db:/app/valuecell.db \
  -v $(pwd)/.knowledgebase:/app/.knowledgebase \
  -v $(pwd)/.env:/app/.env \
  valuecell
```

## 访问应用

- **Web界面**: 打开浏览器访问 [http://localhost:1420](http://localhost:1420)
- **日志**: 查看 `logs/` 目录获取详细日志信息

## 常用命令

### 查看容器状态

```bash
docker ps
```

### 查看日志

```bash
# 查看所有日志
docker logs valuecell

# 实时查看日志
docker logs -f valuecell
```

### 停止服务

```bash
# 使用Docker Compose
docker compose down

# 或者直接停止容器
docker stop valuecell
```

### 重启服务

```bash
# 使用Docker Compose
docker compose restart

# 或者直接重启容器
docker restart valuecell
```

## 数据持久化

以下目录已配置为持久化存储：

- `logs/` - 应用日志
- `lancedb/` - 向量数据库
- `valuecell.db` - SQLite数据库
- `.knowledgebase/` - 知识库数据

## 注意事项

1. **首次启动**：首次启动时，系统会自动初始化数据库，可能需要一些时间。

2. **环境变量**：确保正确配置`.env`文件，至少需要一个LLM提供商的API密钥。

3. **端口冲突**：如果1420或8002端口已被占用，可以在docker-compose.yml中修改端口映射（1420:1420 前端，8002:8000 后端）。

4. **内存要求**：建议为容器分配至少4GB内存以确保良好性能。

## 故障排除

### 数据库兼容性问题

如果遇到数据库兼容性错误，可以尝试删除以下目录后重新启动：

```bash
rm -rf lancedb/ valuecell.db .knowledgebase/
```

### 检查服务状态

```bash
# 查看容器内进程
docker exec -it valuecell ps aux

# 进入容器进行调试
docker exec -it valuecell bash
```

### 查看网络配置

```bash
docker network inspect bridge
```