# 基础镜像 - 使用Python 3.12官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NODE_ENV=development \
    PATH="$PATH:/root/.bun/bin:/root/.local/bin"

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    ca-certificates \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# 安装Bun
RUN curl -fsSL https://bun.sh/install | bash

# 安装uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
RUN bun --version && uv --version

# 复制项目文件
COPY . .

# 创建.env文件（从示例文件复制）
RUN cp .env.example .env

# 安装Python依赖
RUN cd python && \
    uv venv --python 3.12 && \
    uv sync --group dev && \
    uvx playwright install --with-deps chromium && \
    # 安装第三方依赖
    cd third_party/ai-hedge-fund && \
    uv venv --python 3.12 && \
    uv sync && \
    cd ../TradingAgents && \
    uv venv --python 3.12 && \
    uv sync

# 安装前端依赖
RUN cd frontend && bun install

# 暴露端口
EXPOSE 1420 8000

# 设置启动脚本
CMD ["bash", "start.sh"]