# 爆款视频复刻智能体 Dockerfile

# 使用Python官方镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建必要的目录
RUN mkdir -p data/input_videos data/output_videos data/user_images data/temp models

# 下载预训练模型
RUN mkdir -p models/face_detection && \
    cd models/face_detection && \
    wget https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip && \
    unzip buffalo_l.zip && \
    rm buffalo_l.zip

RUN mkdir -p models/face_swap && \
    cd models/face_swap && \
    wget https://github.com/harisreedhar/InsightFace-Swap/releases/download/v1.0.0/inswapper_128.onnx

# 设置权限
RUN chmod +x main.py

# 暴露API端口
EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 运行应用
CMD ["python", "main.py", "--api", "--port", "8000"]