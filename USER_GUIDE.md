# 爆款视频复刻智能体 - 用户指南

## 概述

爆款视频复刻智能体是一个完整的AI驱动系统，能够自动复刻爆款短视频。系统通过以下步骤工作：

1. **下载目标视频** - 从抖音、快手等平台下载视频
2. **分析视频内容** - 检测人脸、识别语音、分析场景
3. **重写文案** - 使用AI模型修改文案，保持原意但改变表达
4. **替换人脸** - 将视频中的人物替换为用户提供的人物
5. **编辑视频** - 添加新字幕、调整音频、优化质量
6. **生成新视频** - 输出复刻后的视频文件

## 快速开始

### 安装

#### 方法1: 使用预构建的可执行文件（推荐）

1. 从[发布页面](https://github.com/openclaw/video-replication-agent/releases)下载最新版本
2. 解压到任意目录
3. 运行 `VideoReplicationAgent.exe` (Windows) 或 `VideoReplicationAgent` (Linux/macOS)

#### 方法2: 从源码安装

```bash
# 克隆仓库
git clone https://github.com/openclaw/video-replication-agent.git
cd video-replication-agent

# 安装依赖
pip install -r requirements.txt

# 下载模型文件（可选，首次运行会自动下载）
python download_models.py
```

#### 方法3: 使用Docker

```bash
# 拉取镜像
docker pull openclaw/video-replication-agent:latest

# 运行容器
docker run -p 8000:8000 -v $(pwd)/data:/app/data openclaw/video-replication-agent
```

### 基本使用

#### 命令行模式

```bash
# 基本用法
python main.py --url "视频链接" --image "用户图片.jpg" --output "输出视频.mp4"

# 指定文案风格
python main.py --url "视频链接" --image "用户图片.jpg" --style "humorous"

# 禁用某些功能
python main.py --url "视频链接" --image "用户图片.jpg" --no-face-swap --no-subtitles

# 查看所有选项
python main.py --help
```

#### GUI模式

```bash
# 启动图形界面
python main.py --gui
```

图形界面提供以下功能：
- 直观的视频链接和图片选择
- 实时预览用户图片
- 可配置的复刻选项
- 处理进度显示
- 详细的处理日志

#### API模式

```bash
# 启动API服务
python main.py --api --port 8000
```

API提供RESTful接口，支持：
- 视频复刻
- 人脸替换
- 文案重写
- 视频分析

## 详细功能

### 1. 视频下载

支持平台：
- 抖音 (Douyin)
- 快手 (Kuaishou)
- TikTok
- YouTube
- Bilibili
- Instagram
- Twitter/X

```python
from src.video_downloader import get_downloader

downloader = get_downloader()
video_info = downloader.download("https://www.douyin.com/video/123")
```

### 2. 视频分析

分析功能包括：
- 人脸检测和识别
- 语音识别（提取文案）
- 场景分析
- 视频基本信息提取

```python
from src.video_analyzer import get_analyzer

analyzer = get_analyzer()
analysis = analyzer.analyze("video.mp4")
```

### 3. 文案重写

支持风格：
- `humorous` - 幽默风趣
- `formal` - 正式专业
- `casual` - 轻松随意
- `persuasive` - 有说服力
- `concise` - 简洁明了
- `creative` - 创意新颖

```python
from src.text_rewriter import get_rewriter, RewriteConfig, RewriteStyle

rewriter = get_rewriter()
result = rewriter.rewrite("原始文案", RewriteConfig(style=RewriteStyle.HUMOROUS))
```

### 4. 人脸替换

基于InsightFace的人脸替换技术：
- 多人脸检测
- 表情保持
- 光照调整
- 边界平滑

```python
from src.face_swapper import get_swapper

swapper = get_swapper()
result = swapper.swap_faces_in_video("source.jpg", "target.mp4", "output.mp4")
```

### 5. 视频编辑

编辑功能：
- 添加字幕
- 调整音频
- 修改分辨率
- 添加水印
- 视频合并

```python
from src.video_editor import get_editor

editor = get_editor()
result = editor.edit_video("input.mp4", "output.mp4", subtitles=[...])
```

## 高级配置

### 配置文件

编辑 `config.py` 文件可以修改：

```python
# 模型配置
MODEL_CONFIG = {
    "face_detection": {
        "model_path": "models/face_detection/buffalo_l",
        "provider": "CUDAExecutionProvider",  # 使用GPU加速
    },
    # ...
}

# 视频处理配置
VIDEO_CONFIG = {
    "target_resolution": (1080, 1920),  # 目标分辨率
    "target_fps": 30,  # 目标帧率
    # ...
}

# API配置
API_CONFIG = {
    "openai": {
        "api_key": "your-api-key",  # 设置API密钥
        # ...
    },
    # ...
}
```

### 批量处理

```python
from src.video_replicator import VideoReplicator

replicator = VideoReplicator()

# 批量复刻
result = replicator.batch_replicate(
    video_urls=["url1", "url2", "url3"],
    user_images=["img1.jpg", "img2.jpg", "img3.jpg"],
    output_dir="output/"
)
```

### 自定义模型

1. 下载模型文件到 `models/` 目录
2. 在 `config.py` 中更新模型路径
3. 重启应用

## 性能优化

### GPU加速

如果系统有NVIDIA GPU：

1. 安装CUDA工具包
2. 安装cuDNN
3. 确保PyTorch支持CUDA
4. 在配置中启用GPU：

```python
MODEL_CONFIG["face_detection"]["provider"] = "CUDAExecutionProvider"
MODEL_CONFIG["text_rewrite"]["device"] = "cuda"
```

### 内存优化

对于大视频处理：

```python
# 降低处理质量以提高速度
config = ReplicationConfig(
    face_swap_config=FaceSwapConfig(
        blend_ratio=0.6,  # 降低融合质量
        max_faces=2  # 限制人脸数量
    ),
    video_edit_config=VideoEditConfig(
        quality="medium"  # 中等质量
    )
)
```

### 并行处理

```python
import concurrent.futures

def process_video(url, image):
    replicator = VideoReplicator()
    return replicator.replicate(url, image)

# 并行处理多个视频
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(process_video, url, img) for url, img in zip(urls, images)]
    results = [f.result() for f in futures]
```

## 故障排除

### 常见问题

#### 1. 视频下载失败
- 检查网络连接
- 确认视频链接有效
- 尝试使用代理
- 更新yt-dlp: `pip install -U yt-dlp`

#### 2. 人脸替换效果不佳
- 确保源图片人脸清晰
- 调整融合比例：`--blend-ratio 0.7`
- 尝试不同的光照调整设置
- 使用更高质量的源图片

#### 3. 文案重写不自然
- 尝试不同的风格：`--style formal`
- 调整温度参数：在配置中修改 `temperature`
- 使用更强大的模型：更新模型配置

#### 4. 内存不足
- 降低视频分辨率
- 减少同时处理的任务数
- 增加系统虚拟内存
- 使用更小的模型

#### 5. 处理速度慢
- 启用GPU加速
- 降低处理质量
- 减少分析帧数
- 使用更快的模型

### 日志查看

```bash
# 查看应用日志
tail -f logs/app.log

# 启用调试模式
python main.py --url "..." --image "..." --debug

# 查看详细错误信息
export LOG_LEVEL=DEBUG
python main.py ...
```

## 部署指南

### 单机部署

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 下载模型
python download_models.py

# 3. 创建服务文件（Linux）
sudo cp video-replication-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable video-replication-agent
sudo systemctl start video-replication-agent
```

### Docker部署

```bash
# 使用Docker Compose
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 云部署

#### AWS EC2
1. 启动GPU实例（推荐g4dn.xlarge）
2. 安装Docker
3. 拉取镜像并运行

#### Google Cloud Run
1. 构建容器镜像
2. 部署到Cloud Run
3. 配置自动扩缩

#### Azure Container Instances
1. 创建容器实例
2. 配置GPU支持
3. 部署应用

## 安全注意事项

### 数据隐私
- 处理后的视频默认保存在本地
- 可以配置加密存储
- 支持自动清理临时文件

### API安全
- 建议使用HTTPS
- 配置API密钥认证
- 设置访问频率限制
- 启用请求日志

### 内容合规
- 遵守平台使用条款
- 尊重原创内容版权
- 仅供学习和研究使用
- 不用于商业侵权用途

## 更新和维护

### 更新应用

```bash
# 从源码更新
git pull origin main
pip install -U -r requirements.txt

# 从Docker更新
docker pull openclaw/video-replication-agent:latest
docker-compose down
docker-compose up -d
```

### 备份数据

```bash
# 备份配置和模型
tar -czf backup-$(date +%Y%m%d).tar.gz config.py models/ data/

# 恢复备份
tar -xzf backup-20240326.tar.gz
```

### 监控和告警

```bash
# 健康检查
curl http://localhost:8000/health

# 性能监控
curl http://localhost:8000/metrics

# 日志监控
tail -f logs/app.log | grep -E "(ERROR|WARNING)"
```

## 技术支持

### 获取帮助
- 查看[文档](https://docs.openclaw.ai/video-replication-agent)
- 提交[Issue](https://github.com/openclaw/video-replication-agent/issues)
- 加入[Discord社区](https://discord.gg/clawd)

### 报告问题
提供以下信息有助于解决问题：
1. 操作系统和Python版本
2. 错误日志
3. 复现步骤
4. 相关配置

### 贡献代码
欢迎提交Pull Request：
1. Fork仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证。详见[LICENSE](LICENSE)文件。

## 免责声明

本工具仅供学习和研究使用。用户需遵守相关法律法规和平台条款，对使用本工具产生的任何后果自行负责。