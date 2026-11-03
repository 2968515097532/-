# 爆款视频复刻智能体系统

## 概述
一个完整的智能体系统，用于自动复刻爆款短视频。系统能够：
1. 下载目标视频
2. 分析视频内容（文案、人物、场景）
3. 使用免费大模型修改文案
4. 替换视频中的人物（使用用户提供的图片）
5. 生成新的复刻视频
6. 打包成开箱即用的应用程序

## 系统架构

```
video_replication_agent/
├── main.py                    # 主程序入口
├── config.py                  # 配置文件
├── requirements.txt           # 依赖包
├── README.md                  # 说明文档
├── setup.py                   # 打包配置
├── src/
│   ├── __init__.py
│   ├── video_downloader.py    # 视频下载模块
│   ├── video_analyzer.py      # 视频分析模块
│   ├── text_rewriter.py       # 文案重写模块
│   ├── face_swapper.py        # 人脸替换模块
│   ├── video_editor.py        # 视频编辑模块
│   └── ui/                    # 用户界面
│       ├── main_window.py
│       └── styles.qss
├── models/                    # 模型文件
│   ├── face_detection/
│   └── face_swap/
├── data/                      # 数据目录
│   ├── input_videos/          # 输入视频
│   ├── output_videos/         # 输出视频
│   ├── user_images/           # 用户图片
│   └── temp/                  # 临时文件
└── tests/                     # 测试文件
```

## 功能模块

### 1. 视频下载模块
- 支持主流短视频平台（抖音、快手、TikTok等）
- 使用yt-dlp进行视频下载
- 提取视频元数据（标题、描述、标签）

### 2. 视频分析模块
- 使用OpenCV分析视频帧
- 人脸检测和识别
- 场景分析
- 音频提取和语音识别

### 3. 文案重写模块
- 集成免费大模型（如ChatGLM、Qwen等）
- 保持原意但改变表达方式
- 支持多种风格（幽默、正式、简洁等）

### 4. 人脸替换模块
- 使用InsightFace或ROOP进行人脸替换
- 支持多人脸检测和替换
- 保持表情和光照一致性

### 5. 视频编辑模块
- 使用MoviePy进行视频编辑
- 添加新的字幕和文案
- 音频处理和混音
- 视频质量优化

## 技术栈
- Python 3.8+
- PyTorch / TensorFlow
- OpenCV
- MoviePy
- yt-dlp
- InsightFace / ROOP
- 免费大模型API（ChatGLM、Qwen等）
- PyQt6（GUI界面）

## 使用方式

### 命令行模式
```bash
python main.py --url "视频链接" --image "用户图片.jpg" --output "输出视频.mp4"
```

### GUI模式
```bash
python main.py --gui
```

### API模式
```python
from src.video_replicator import VideoReplicator

replicator = VideoReplicator()
result = replicator.replicate(
    video_url="视频链接",
    user_image="用户图片.jpg",
    output_path="输出视频.mp4"
)
```

## 打包发布
使用PyInstaller打包成可执行文件：
```bash
pyinstaller --onefile --windowed main.py
```

## 注意事项
1. 遵守平台使用条款
2. 尊重原创内容
3. 仅供学习和研究使用
4. 注意版权问题