# 爆款视频复刻智能体 - 快速开始指南

## 🚀 5分钟快速开始

### 步骤1: 下载项目
```bash
# 克隆项目（如果你有Git）
git clone <repository-url>
cd video-replication-agent

# 或者直接下载ZIP包并解压
```

### 步骤2: 快速初始化
```bash
# 运行快速初始化脚本
python init_project.py --quick
```

### 步骤3: 启动图形界面
```bash
# 启动用户友好的图形界面
python run.py gui
```

### 步骤4: 开始使用！
1. 在图形界面中输入视频链接
2. 选择用户图片
3. 点击"开始复刻"按钮
4. 等待处理完成
5. 查看和下载结果

## 📋 系统要求

### 最低配置
- **操作系统**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **处理器**: 4核CPU
- **内存**: 8GB RAM
- **存储**: 20GB 可用空间
- **Python**: 3.8 或更高版本

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 20.04+
- **处理器**: 8核CPU
- **内存**: 16GB RAM
- **存储**: 50GB 可用空间
- **GPU**: NVIDIA GPU (支持CUDA)
- **Python**: 3.10 或更高版本

## 🔧 完整安装

### 1. 基础安装
```bash
# 1. 克隆或下载项目
git clone <repository-url>
cd video-replication-agent

# 2. 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 下载模型
python download_models.py

# 5. 初始化配置
python init_project.py
```

### 2. Docker安装
```bash
# 使用Docker Compose（推荐）
docker-compose up -d

# 或者直接运行Docker容器
docker run -p 8000:8000 openclaw/video-replication-agent
```

### 3. 一键安装脚本
```bash
# Windows
start.bat install

# Linux/macOS
./start.sh install
```

## 🎯 使用方式

### 1. 命令行模式（适合开发者）
```bash
# 基本使用
python run.py cli --url "视频链接" --image "用户图片.jpg"

# 完整参数
python run.py cli \
  --url "https://example.com/video" \
  --image "user.jpg" \
  --output "result.mp4" \
  --style "幽默" \
  --resolution "1080p" \
  --quality "high"

# 批量处理
python run.py batch \
  --input "videos.txt" \
  --images "images_folder/" \
  --output "results/"
```

### 2. 图形界面模式（适合普通用户）
```bash
# 启动GUI
python run.py gui

# 或者直接运行
python main.py
```

### 3. API服务模式（适合集成）
```bash
# 启动API服务
python run.py api --port 8000

# API文档
# 访问 http://localhost:8000/docs
```

### 4. 完整服务模式（生产环境）
```bash
# 启动完整服务（API + 管理面板）
python run.py service

# 访问地址
# API: http://localhost:8000
# 管理面板: http://localhost:8080/admin
```

## 📁 项目结构

```
video_replication_agent/
├── 📁 src/                    # 核心源代码
│   ├── video_downloader.py   # 视频下载模块
│   ├── video_analyzer.py     # 视频分析模块
│   ├── text_rewriter.py      # 文案重写模块
│   ├── face_swapper.py       # 人脸替换模块
│   ├── video_editor.py       # 视频编辑模块
│   ├── video_replicator.py   # 主协调器
│   └── 📁 ui/                # 图形界面
├── 📁 api/                   # API服务
├── 📁 web_admin/             # 管理面板
├── 📁 scripts/               # 工具脚本
├── 📁 examples/              # 使用示例
├── 📁 tests/                 # 单元测试
├── 📄 main.py               # 主程序入口
├── 📄 run.py                # 统一运行脚本
├── 📄 config.py             # 配置文件
├── 📄 requirements.txt      # 依赖包
└── 📄 README.md             # 项目说明
```

## ⚙️ 配置说明

### 配置文件位置
- `config.json` - JSON格式配置文件
- `config.yaml` - YAML格式配置文件
- `.env` - 环境变量文件

### 主要配置项
```json
{
  "app": {
    "name": "爆款视频复刻智能体",
    "version": "1.0.0",
    "debug": false
  },
  "models": {
    "face_detection": {
      "model_path": "models/face_detection/det_10g.onnx",
      "provider": "CPUExecutionProvider"
    },
    "face_swap": {
      "model_path": "models/face_swap/inswapper_128.onnx"
    },
    "text_rewrite": {
      "model_name": "Qwen/Qwen2.5-1.5B-Instruct"
    }
  },
  "storage": {
    "data_dir": "data",
    "models_dir": "models",
    "logs_dir": "logs"
  }
}
```

## 🔍 功能演示

### 演示所有功能
```bash
# 运行完整演示
python scripts/demo.py

# 交互式演示
python scripts/demo.py --interactive
```

### 测试系统
```bash
# 运行系统测试
python scripts/test_system.py

# 生成测试报告
python scripts/test_system.py --report
```

## 🛠️ 工具脚本

### 1. 模型优化
```bash
# 优化所有模型
python scripts/optimize_models.py --all

# 优化人脸检测模型
python scripts/optimize_models.py --face-size medium

# 量化文本模型
python scripts/optimize_models.py --quantize-text
```

### 2. 视频质量分析
```bash
# 分析视频质量
python scripts/video_quality.py analyze input.mp4

# 优化视频质量
python scripts/video_quality.py optimize input.mp4 output.mp4

# 批量优化
python scripts/video_quality.py batch input_folder/ output_folder/
```

### 3. 系统监控
```bash
# 查看系统状态
python scripts/monitor.py status

# 监控实时性能
python scripts/monitor.py live

# 生成性能报告
python scripts/monitor.py report
```

## 📊 性能调优

### 提升处理速度
```bash
# 1. 启用GPU加速（如果有NVIDIA GPU）
# 编辑 config.json，设置：
# "models.face_detection.provider": "CUDAExecutionProvider"

# 2. 使用轻量级模型
python scripts/optimize_models.py --face-size small

# 3. 调整线程数
# 编辑 config.json，设置：
# "max_workers": 4
```

### 减少内存使用
```bash
# 1. 量化模型
python scripts/optimize_models.py --quantize

# 2. 使用模型剪枝
python scripts/optimize_models.py --prune

# 3. 调整批处理大小
# 编辑 config.json，设置：
# "batch_size": 1
```

## 🚨 故障排除

### 常见问题

#### 1. 依赖安装失败
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或者使用conda
conda create -n video-replication python=3.10
conda activate video-replication
```

#### 2. 模型下载失败
```bash
# 手动下载模型
# 1. 访问模型下载页面
# 2. 下载模型文件到 models/ 目录
# 3. 更新配置文件中的模型路径
```

#### 3. GPU不可用
```bash
# 检查CUDA安装
python -c "import torch; print(torch.cuda.is_available())"

# 如果返回False，请安装CUDA版本的PyTorch
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

#### 4. 内存不足
```bash
# 减少批处理大小
# 编辑 config.json，设置：
# "batch_size": 1
# "max_workers": 2

# 使用轻量级模型
python scripts/optimize_models.py --face-size small
```

### 获取帮助
```bash
# 查看帮助文档
python run.py --help
python main.py --help

# 查看具体命令帮助
python run.py cli --help
python run.py api --help
```

## 📈 进阶使用

### 自定义模型
1. 将自定义模型文件放入 `models/` 目录
2. 更新 `config.json` 中的模型路径
3. 重启应用

### 扩展功能
1. 在 `src/` 目录中添加新模块
2. 在 `video_replicator.py` 中集成新功能
3. 更新配置和API接口

### 集成到其他系统
```python
# Python集成示例
from src.video_replicator import VideoReplicator

replicator = VideoReplicator()
result = replicator.process_video(
    video_url="视频链接",
    user_image_path="用户图片.jpg",
    output_path="输出视频.mp4"
)
```

## 📞 技术支持

### 文档资源
- `README.md` - 项目概述
- `USER_GUIDE.md` - 详细用户指南
- `INSTALL.md` - 安装和配置指南
- `PROJECT_SUMMARY.md` - 项目技术总结

### 获取帮助
1. 查看文档和示例
2. 运行演示了解功能
3. 查看错误日志（`logs/` 目录）
4. 提交Issue报告问题

### 社区支持
- **GitHub**: 项目仓库和Issue跟踪
- **Discord**: 实时交流和讨论
- **文档网站**: 在线文档和教程

## 🎉 开始创作！

现在你已经准备好使用爆款视频复刻智能体了！

### 第一步：尝试简单示例
```bash
# 使用示例视频和图片
python examples/basic_usage.py
```

### 第二步：处理你的第一个视频
```bash
# 使用图形界面
python run.py gui

# 或者使用命令行
python run.py cli --url "你的视频链接" --image "你的图片.jpg"
```

### 第三步：探索高级功能
```bash
# 批量处理多个视频
python run.py batch --input "video_list.txt"

# 启动API服务供其他应用调用
python run.py api

# 使用管理面板监控系统
python run.py admin
```

### 第四步：定制和优化
1. 根据需求调整配置
2. 优化模型性能
3. 扩展系统功能
4. 集成到工作流程中

---

**祝您使用愉快！如有任何问题，请查阅文档或寻求社区帮助。** 🎬✨

**爆款视频复刻智能体** - 让视频创作更简单，让创意表达更自由！