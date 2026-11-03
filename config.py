"""
配置文件 - 使用新的配置加载系统
"""

import os
from pathlib import Path

# 使用新的配置加载器
from config_loader import get_config, setup_environment

# 初始化配置
config = get_config()

# 向后兼容的导出
# 基础路径
BASE_DIR = Path(config.base_dir)
DATA_DIR = Path(config.storage.data_dir)
MODELS_DIR = Path(config.storage.models_dir)
OUTPUT_DIR = DATA_DIR / "output_videos"
INPUT_DIR = DATA_DIR / "input_videos"
USER_IMAGES_DIR = DATA_DIR / "user_images"
TEMP_DIR = Path(config.storage.temp_dir)

# 创建必要的目录
for dir_path in [DATA_DIR, MODELS_DIR, OUTPUT_DIR, INPUT_DIR, USER_IMAGES_DIR, TEMP_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# 模型配置（向后兼容）
MODEL_CONFIG = {
    "face_detection": config.models.face_detection,
    "face_swap": config.models.face_swap,
    "text_rewrite": config.models.text_rewrite
}

# 视频处理配置（向后兼容）
VIDEO_CONFIG = {
    "max_duration": config.video.max_duration,
    "target_resolution": config.video.target_resolution,
    "target_fps": config.video.target_fps,
    "audio_bitrate": config.video.audio_bitrate,
    "video_bitrate": config.video.video_bitrate
}

# 下载配置（向后兼容）
DOWNLOAD_CONFIG = {
    "timeout": config.download.timeout,
    "max_retries": config.download.max_retries,
    "user_agent": config.download.user_agent
}

# API配置（向后兼容）
API_CONFIG = config.api.__dict__

# 日志配置（向后兼容）
LOG_CONFIG = config.logs.__dict__

# 界面配置（向后兼容）
UI_CONFIG = config.ui.__dict__

# 检查CUDA可用性
try:
    import torch
    CUDA_AVAILABLE = torch.cuda.is_available()
except ImportError:
    CUDA_AVAILABLE = False

# 更新模型配置中的设备
if CUDA_AVAILABLE and config.models.face_detection["provider"] == "CUDAExecutionProvider":
    MODEL_CONFIG["face_detection"]["provider"] = "CUDAExecutionProvider"
    MODEL_CONFIG["face_swap"]["provider"] = "CUDAExecutionProvider"
    MODEL_CONFIG["text_rewrite"]["device"] = "cuda"
else:
    MODEL_CONFIG["face_detection"]["provider"] = "CPUExecutionProvider"
    MODEL_CONFIG["face_swap"]["provider"] = "CPUExecutionProvider"
    MODEL_CONFIG["text_rewrite"]["device"] = "cpu"

# 导出配置检查函数
def check_config():
    """检查配置"""
    print("=" * 60)
    print("爆款视频复刻智能体 - 配置检查")
    print("=" * 60)
    
    # 检查目录
    directories = {
        "数据目录": DATA_DIR,
        "模型目录": MODELS_DIR,
        "输出目录": OUTPUT_DIR,
        "输入目录": INPUT_DIR,
        "用户图片目录": USER_IMAGES_DIR,
        "临时目录": TEMP_DIR
    }
    
    print("\n目录检查:")
    for name, path in directories.items():
        if path.exists():
            print(f"  ✓ {name}: {path}")
        else:
            print(f"  ✗ {name}: {path} (不存在)")
    
    # 检查模型文件
    print("\n模型检查:")
    models = {
        "人脸检测模型": Path(MODEL_CONFIG["face_detection"]["model_path"]),
        "人脸替换模型": Path(MODEL_CONFIG["face_swap"]["model_path"])
    }
    
    for name, path in models.items():
        if path.exists():
            print(f"  ✓ {name}: {path}")
        else:
            print(f"  ✗ {name}: {path} (不存在)")
    
    # 检查CUDA
    print("\n硬件检查:")
    print(f"  CUDA可用: {'✓' if CUDA_AVAILABLE else '✗'}")
    if CUDA_AVAILABLE:
        print(f"  GPU设备: {torch.cuda.get_device_name(0)}")
    
    # 检查Python版本
    import sys
    print(f"  Python版本: {sys.version}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # 运行配置检查
    check_config()