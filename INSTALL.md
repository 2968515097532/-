# 安装指南

## 系统要求

### 最低配置
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **处理器**: 4核CPU (Intel i5或同等)
- **内存**: 8GB RAM
- **存储**: 20GB可用空间
- **Python**: 3.8或更高版本

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **处理器**: 8核CPU (Intel i7或同等)
- **内存**: 16GB RAM
- **显卡**: NVIDIA GPU (GTX 1060或更高，支持CUDA)
- **存储**: 50GB可用空间
- **Python**: 3.10或更高版本

## 快速安装

### 方法1: 使用安装脚本 (推荐)

#### Windows
```powershell
# 1. 下载项目
git clone https://github.com/openclaw/video-replication-agent.git
cd video-replication-agent

# 2. 运行安装脚本
.\start.bat --help
```

#### Linux/macOS
```bash
# 1. 下载项目
git clone https://github.com/openclaw/video-replication-agent.git
cd video-replication-agent

# 2. 给脚本执行权限
chmod +x start.sh download_models.py

# 3. 运行安装脚本
./start.sh --help
```

### 方法2: 手动安装

```bash
# 1. 克隆项目
git clone https://github.com/openclaw/video-replication-agent.git
cd video-replication-agent

# 2. 创建虚拟环境 (推荐)
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型
python download_models.py

# 5. 创建必要目录
mkdir -p data/{input_videos,output_videos,user_images,temp}
mkdir -p models/{face_detection,face_swap,text}
mkdir logs

# 6. 测试安装
python -c "import torch; print(f'PyTorch版本: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV版本: {cv2.__version__}')"
```

### 方法3: 使用Docker

```bash
# 1. 拉取镜像
docker pull openclaw/video-replication-agent:latest

# 2. 运行容器
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  openclaw/video-replication-agent

# 3. 或者使用Docker Compose
docker-compose up -d
```

## 详细安装步骤

### Windows系统

#### 步骤1: 安装Python
1. 访问 https://www.python.org/downloads/
2. 下载Python 3.10+安装程序
3. 安装时勾选"Add Python to PATH"
4. 验证安装: `python --version`

#### 步骤2: 安装Git
1. 访问 https://git-scm.com/download/win
2. 下载并安装Git
3. 验证安装: `git --version`

#### 步骤3: 安装FFmpeg (视频处理必需)
1. 访问 https://ffmpeg.org/download.html
2. 下载Windows版本
3. 解压到 `C:\ffmpeg`
4. 添加 `C:\ffmpeg\bin` 到系统PATH

#### 步骤4: 安装CUDA (GPU加速，可选但推荐)
1. 访问 https://developer.nvidia.com/cuda-downloads
2. 下载CUDA Toolkit 11.8+
3. 按照向导安装
4. 验证安装: `nvcc --version`

### macOS系统

#### 步骤1: 安装Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 步骤2: 安装依赖
```bash
# 安装Python
brew install python@3.10

# 安装FFmpeg
brew install ffmpeg

# 安装其他工具
brew install git wget
```

#### 步骤3: 配置Python环境
```bash
# 更新pip
python3 -m pip install --upgrade pip

# 安装虚拟环境工具
python3 -m pip install virtualenv
```

### Linux系统 (Ubuntu/Debian)

#### 步骤1: 更新系统
```bash
sudo apt update
sudo apt upgrade -y
```

#### 步骤2: 安装依赖
```bash
# 安装Python和工具
sudo apt install python3.10 python3.10-venv python3-pip -y

# 安装FFmpeg
sudo apt install ffmpeg -y

# 安装开发工具
sudo apt install git wget curl build-essential -y

# 安装CUDA (如果有NVIDIA GPU)
sudo apt install nvidia-cuda-toolkit -y
```

## 模型下载

### 自动下载
```bash
# 下载所有模型
python download_models.py

# 下载特定模型
python download_models.py --model face_detection
python download_models.py --model face_swap
python download_models.py --model text_model

# 强制重新下载
python download_models.py --force
```

### 手动下载
如果自动下载失败，可以手动下载：

1. **人脸检测模型** (buffalo_l):
   - 下载: https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip
   - 解压到: `models/face_detection/`

2. **人脸替换模型** (inswapper_128):
   - 下载: https://github.com/harasreedhar/InsightFace-Swap/releases/download/v1.0.0/inswapper_128.onnx
   - 保存到: `models/face_swap/inswapper_128.onnx`

3. **文本模型** (可选):
   - 下载: https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct
   - 保存到: `models/text/`

## 验证安装

### 基本验证
```bash
# 检查Python版本
python --version

# 检查依赖
python -c "import torch; print('PyTorch:', torch.__version__, 'CUDA:', torch.cuda.is_available())"
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import moviepy; print('MoviePy: OK')"

# 检查模型
python -c "
import os
print('人脸检测模型:', '存在' if os.path.exists('models/face_detection/det_10g.onnx') else '缺失')
print('人脸替换模型:', '存在' if os.path.exists('models/face_swap/inswapper_128.onnx') else '缺失')
"
```

### 运行测试
```bash
# 运行单元测试
python -m pytest tests/test_basic.py -v

# 运行示例
python examples/basic_usage.py
```

### 功能测试
```bash
# 测试文案重写
python -c "
from src.text_rewriter import TextRewriter
rewriter = TextRewriter(use_local_model=False)
result = rewriter.rewrite('这是一个测试文案')
print('文案重写测试:', '成功' if result['rewritten_text'] else '失败')
"

# 测试视频编辑器
python -c "
import numpy as np
import cv2
import tempfile
import os
from src.video_editor import VideoEditor

# 创建测试视频
temp_dir = tempfile.mkdtemp()
test_video = os.path.join(temp_dir, 'test.mp4')
frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(test_video, fourcc, 1.0, (100, 100))
out.write(frame)
out.release()

# 测试编辑器
editor = VideoEditor()
try:
    result = editor.edit_video(test_video, os.path.join(temp_dir, 'output.mp4'), [])
    print('视频编辑器测试: 成功')
except Exception as e:
    print(f'视频编辑器测试: 失败 - {e}')
"
```

## 常见问题解决

### 问题1: Python版本错误
```
错误: 需要Python 3.8+，但找到的是2.7
```
**解决方案**:
- 确认安装的是Python 3
- 使用 `python3` 命令
- 更新系统PATH

### 问题2: 依赖安装失败
```
错误: 无法找到满足要求的版本
```
**解决方案**:
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或逐个安装
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 问题3: CUDA不可用
```
警告: CUDA不可用，使用CPU模式
```
**解决方案**:
1. 确认安装了NVIDIA驱动
2. 安装CUDA Toolkit
3. 安装cuDNN
4. 重新安装PyTorch:
```bash
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 问题4: 模型下载失败
```
错误: 下载超时或网络错误
```
**解决方案**:
1. 使用代理
2. 手动下载模型
3. 使用备用下载源

### 问题5: 内存不足
```
错误: CUDA out of memory
```
**解决方案**:
1. 减小批处理大小
2. 使用更小的模型
3. 增加虚拟内存
4. 使用CPU模式

## 性能优化

### GPU加速配置
```python
# 在config.py中修改
MODEL_CONFIG = {
    "face_detection": {
        "provider": "CUDAExecutionProvider",  # 使用GPU
    },
    "text_rewrite": {
        "device": "cuda",  # 使用GPU
    }
}
```

### 内存优化
```bash
# 降低视频分辨率
python main.py --url ... --image ... --resolution 720

# 减少人脸检测精度
python main.py --url ... --image ... --detection-threshold 0.3

# 使用更快的模型
python main.py --url ... --image ... --model-fast
```

### 并行处理
```python
# 在代码中启用多线程
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_video, url, img) for url, img in tasks]
```

## 更新和维护

### 更新应用
```bash
# 从源码更新
git pull origin main
pip install -U -r requirements.txt
python download_models.py --force

# 从Docker更新
docker-compose down
docker-compose pull
docker-compose up -d
```

### 备份配置
```bash
# 备份重要文件
tar -czf backup-$(date +%Y%m%d).tar.gz \
  config.py \
  models/ \
  data/output_videos/ \
  logs/
```

### 清理空间
```bash
# 清理临时文件
rm -rf data/temp/*

# 清理日志
find logs/ -name "*.log" -mtime +7 -delete

# 清理旧输出
find data/output_videos/ -name "*.mp4" -mtime +30 -delete
```

## 获取帮助

### 查看文档
```bash
# 查看用户指南
cat USER_GUIDE.md | less

# 查看项目总结
cat PROJECT_SUMMARY.md | less
```

### 命令行帮助
```bash
# 查看主程序帮助
python main.py --help

# 查看启动脚本帮助
./start.sh --help
./start.bat --help
```

### 在线资源
- **官方文档**: https://docs.openclaw.ai/video-replication-agent
- **GitHub仓库**: https://github.com/openclaw/video-replication-agent
- **问题反馈**: https://github.com/openclaw/video-replication-agent/issues
- **社区讨论**: https://discord.gg/clawd

## 下一步

安装完成后，您可以：

1. **快速开始**: 运行 `./start.sh --gui` 启动图形界面
2. **尝试示例**: 运行 `python examples/basic_usage.py`
3. **学习使用**: 阅读 `USER_GUIDE.md`
4. **探索功能**: 查看 `PROJECT_SUMMARY.md`
5. **开始创作**: 使用您的第一个视频进行复刻！

祝您使用愉快！ 🎬✨