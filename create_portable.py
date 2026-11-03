"""
创建便携版应用程序
包含Python解释器和所有依赖
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
import json
from datetime import datetime


def create_portable_package():
    """创建便携版包"""
    print("=" * 60)
    print("爆款视频复刻智能体 - 便携版创建工具")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    portable_dir = project_root / "portable"
    
    # 清理旧目录
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    # 创建目录结构
    print("\n1. 创建目录结构...")
    directories = [
        "app",
        "python",
        "data",
        "models",
        "logs",
        "temp",
        "docs"
    ]
    
    for dir_name in directories:
        (portable_dir / dir_name).mkdir(parents=True, exist_ok=True)
        print(f"  创建目录: {dir_name}")
    
    # 复制应用程序文件
    print("\n2. 复制应用程序文件...")
    
    # 复制Python文件
    python_files = [
        "run.py", "main.py", "config.py", "config_loader.py",
        "download_models.py", "init_project.py"
    ]
    
    for file_name in python_files:
        src = project_root / file_name
        if src.exists():
            dst = portable_dir / "app" / file_name
            shutil.copy2(src, dst)
            print(f"  复制: {file_name}")
    
    # 复制源代码目录
    src_dirs = ["src", "api", "web_admin", "utils", "scripts"]
    for dir_name in src_dirs:
        src = project_root / dir_name
        if src.exists():
            dst = portable_dir / "app" / dir_name
            shutil.copytree(src, dst, dirs_exist_ok=True)
            print(f"  复制目录: {dir_name}")
    
    # 复制文档
    print("\n3. 复制文档...")
    docs_files = [
        "README.md", "USER_GUIDE.md", "LAUNCH_GUIDE.md",
        "QUICK_START.md", "INSTALL.md", "PROJECT_SUMMARY.md",
        "PROJECT_COMPLETE.md", "FINAL_SUMMARY.md", "PACKAGING_GUIDE.md"
    ]
    
    for file_name in docs_files:
        src = project_root / file_name
        if src.exists():
            dst = portable_dir / "docs" / file_name
            shutil.copy2(src, dst)
            print(f"  复制文档: {file_name}")
    
    # 复制配置文件示例
    config_example = project_root / ".env.example"
    if config_example.exists():
        shutil.copy2(config_example, portable_dir / "app" / ".env.example")
        print("  复制配置文件示例")
    
    # 创建启动脚本
    print("\n4. 创建启动脚本...")
    create_launch_scripts(portable_dir)
    
    # 创建配置文件
    print("\n5. 创建配置文件...")
    create_config_files(portable_dir)
    
    # 创建说明文件
    print("\n6. 创建说明文件...")
    create_readme_files(portable_dir)
    
    # 创建ZIP包
    print("\n7. 创建ZIP包...")
    zip_path = create_zip_package(portable_dir)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("🎉 便携版创建完成!")
    print("=" * 60)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"\n📦 生成文件: {zip_path.name} ({size_mb:.1f} MB)")
    
    print("\n📁 目录结构:")
    print("  portable/")
    print("  ├── app/                    # 应用程序文件")
    print("  │   ├── run.py             # 主程序")
    print("  │   ├── config.py          # 配置文件")
    print("  │   ├── src/               # 源代码")
    print("  │   └── ...")
    print("  ├── python/                # Python解释器（需要手动添加）")
    print("  ├── data/                  # 数据目录")
    print("  ├── models/                # 模型目录")
    print("  ├── logs/                  # 日志目录")
    print("  ├── temp/                  # 临时目录")
    print("  ├── docs/                  # 文档")
    print("  ├── start.bat              # Windows启动脚本")
    print("  ├── start.sh               # Linux/macOS启动脚本")
    print("  └── README_PORTABLE.md     # 便携版说明")
    
    print("\n🚀 使用方法:")
    print("  1. 解压 portable.zip")
    print("  2. 安装Python到 portable/python/ 目录")
    print("  3. 运行 start.bat (Windows) 或 start.sh (Linux/macOS)")
    print("  4. 首次运行会自动安装依赖")
    
    print("\n💡 提示:")
    print("  • 需要Python 3.8+")
    print("  • 首次运行需要网络连接安装依赖")
    print("  • 查看 docs/ 目录获取详细指南")
    
    return True


def create_launch_scripts(portable_dir):
    """创建启动脚本"""
    # Windows批处理脚本
    bat_content = """@echo off
REM ========================================
REM  爆款视频复刻智能体 - 便携版启动脚本
REM ========================================

echo.
echo 爆款视频复刻智能体 - 便携版
echo ========================================
echo.

REM 设置工作目录
cd /d "%~dp0"

REM 检查Python
if exist "python\\python.exe" (
    set PYTHON_PATH=python\\python.exe
    echo 使用内置Python解释器
) else (
    REM 尝试系统Python
    where python >nul 2>&1
    if %errorlevel% == 0 (
        set PYTHON_PATH=python
        echo 使用系统Python解释器
    ) else (
        echo 错误: 未找到Python解释器!
        echo.
        echo 请执行以下步骤:
        echo 1. 安装Python 3.8或更高版本
        echo 2. 将Python安装到 portable\\python\\ 目录
        echo 3. 或确保系统PATH中包含Python
        echo.
        pause
        exit /b 1
    )
)

REM 检查依赖
if not exist "app\\requirements_installed.flag" (
    echo.
    echo 首次运行，安装依赖...
    %PYTHON_PATH% -m pip install --upgrade pip
    %PYTHON_PATH% -m pip install -r app\\requirements.txt
    echo. > "app\\requirements_installed.flag"
    echo 依赖安装完成!
)

REM 设置环境变量
set PYTHONPATH=%~dp0app
set VIDEO_REPLICATION_HOME=%~dp0

REM 运行应用程序
echo.
echo 启动应用程序...
echo.
%PYTHON_PATH% app\\run.py %*

echo.
if "%1"=="" pause
"""
    
    # Linux/macOS Shell脚本
    sh_content = """#!/bin/bash
# ========================================
#  爆款视频复刻智能体 - 便携版启动脚本
# ========================================

echo ""
echo "爆款视频复刻智能体 - 便携版"
echo "========================================"
echo ""

# 设置工作目录
cd "$(dirname "$0")"

# 检查Python
if [ -f "python/bin/python3" ]; then
    PYTHON_PATH="python/bin/python3"
    echo "使用内置Python解释器"
elif [ -f "python/python" ]; then
    PYTHON_PATH="python/python"
    echo "使用内置Python解释器"
else
    # 尝试系统Python
    if command -v python3 &> /dev/null; then
        PYTHON_PATH="python3"
        echo "使用系统Python解释器"
    elif command -v python &> /dev/null; then
        PYTHON_PATH="python"
        echo "使用系统Python解释器"
    else
        echo "错误: 未找到Python解释器!"
        echo ""
        echo "请执行以下步骤:"
        echo "1. 安装Python 3.8或更高版本"
        echo "2. 将Python安装到 portable/python/ 目录"
        echo "3. 或确保系统PATH中包含Python"
        echo ""
        exit 1
    fi
fi

# 检查依赖
if [ ! -f "app/requirements_installed.flag" ]; then
    echo ""
    echo "首次运行，安装依赖..."
    $PYTHON_PATH -m pip install --upgrade pip
    $PYTHON_PATH -m pip install -r app/requirements.txt
    touch "app/requirements_installed.flag"
    echo "依赖安装完成!"
fi

# 设置环境变量
export PYTHONPATH="$(pwd)/app"
export VIDEO_REPLICATION_HOME="$(pwd)"

# 运行应用程序
echo ""
echo "启动应用程序..."
echo ""
$PYTHON_PATH app/run.py "$@"

echo ""
"""
    
    # 写入脚本文件
    bat_file = portable_dir / "start.bat"
    with open(bat_file, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    sh_file = portable_dir / "start.sh"
    with open(sh_file, 'w', encoding='utf-8') as f:
        f.write(sh_content)
    
    # 设置执行权限
    sh_file.chmod(0o755)
    
    print("  创建: start.bat, start.sh")


def create_config_files(portable_dir):
    """创建配置文件"""
    # 创建requirements.txt
    requirements_content = """# 爆款视频复刻智能体 - 依赖包

# 核心依赖
torch>=2.0.0
torchvision>=0.15.0
opencv-python>=4.8.0
moviepy>=1.0.3
yt-dlp>=2023.10.13

# AI模型
insightface>=0.7.3
onnxruntime>=1.15.0
transformers>=4.35.0

# 用户界面
PyQt6>=6.5.0
PyQt6-Qt6>=6.5.0
PyQt6-sip>=13.5.0

# Web服务
fastapi>=0.104.0
uvicorn>=0.24.0
python-multipart>=0.0.6

# 工具库
loguru>=0.7.0
psutil>=5.9.0
numpy>=1.24.0
pillow>=10.0.0
requests>=2.31.0
python-dotenv>=1.0.0
pyyaml>=6.0.0

# 开发工具（可选）
pytest>=7.4.0
black>=23.11.0
"""
    
    requirements_file = portable_dir / "app" / "requirements.txt"
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    # 创建配置示例
    config_example = portable_dir / "app" / "config_portable.json"
    config_content = {
        "app": {
            "name": "爆款视频复刻智能体 - 便携版",
            "version": "1.0.0",
            "portable": True
        },
        "paths": {
            "data_dir": "../data",
            "models_dir": "../models",
            "logs_dir": "../logs",
            "temp_dir": "../temp"
        },
        "first_run": True
    }
    
    with open(config_example, 'w', encoding='utf-8') as f:
        json.dump(config_content, f, indent=2, ensure_ascii=False)
    
    print("  创建: requirements.txt, config_portable.json")


def create_readme_files(portable_dir):
    """创建说明文件"""
    readme_content = f"""# 爆款视频复刻智能体 - 便携版

版本: 1.0.0
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 简介

这是一个便携版的爆款视频复刻智能体，包含完整的应用程序和配置，无需安装即可运行。

## 系统要求

- **操作系统**: Windows 10/11, Linux, macOS
- **Python**: 3.8 或更高版本（可内置或系统安装）
- **内存**: 至少 8GB RAM
- **存储**: 至少 20GB 可用空间

## 快速开始

### Windows用户
1. 解压此ZIP包到任意目录
2. 双击运行 `start.bat`
3. 首次运行会自动安装Python依赖
4. 按照提示操作

### Linux/macOS用户
1. 解压此ZIP包到任意目录
2. 打开终端
3. 运行: `chmod +x start.sh`
4. 运行: `./start.sh`
5. 首次运行会自动安装Python依赖

## 目录结构

```
portable/
├── app/                    # 应用程序文件
│   ├── run.py             # 主程序入口
│   ├── config.py          # 配置文件
│   ├── src/               # 源代码
│   ├── api/               # API服务
│   ├── web_admin/         # 管理面板
│   ├── utils/             # 工具函数
│   ├── scripts/           # 工具脚本
│   ├── requirements.txt   # Python依赖
│   └── config_portable.json # 便携版配置
├── python/                # Python解释器目录（可选）
├── data/                  # 数据目录
├── models/                # AI模型目录
├── logs/                  # 日志目录
├── temp/                  # 临时文件目录
├── docs/                  # 文档
├── start.bat              # Windows启动脚本
├── start.sh               # Linux/macOS启动脚本
└── README_PORTABLE.md     # 本文件
```

## 功能特点

### ✅ 已实现功能
1. **视频下载**: 支持抖音、快手、TikTok等平台
2. **视频分析**: 人脸检测、语音识别、场景分析
3. **文案重写**: 使用免费大模型修改文案
4. **人脸替换**: 高质量人脸替换技术
5. **视频编辑**: 字幕、音频、画质优化
6. **批量处理**: 自动化批量视频复刻
7. **多种界面**: 图形界面、命令行、API服务
8. **管理面板**: Web管理界面，实时监控

### 🚀 使用方式
- **图形界面**: 运行后选择GUI模式
- **命令行**: `start.bat cli --url "视频链接" --image "用户图片"`
- **API服务**: `start.bat api --port 8000`
- **批量处理**: `start.bat batch --input "视频列表.txt"`

## 首次使用指南

### 1. 准备Python环境
- 如果 `python/` 目录为空，需要安装Python
- 可以从 https://www.python.org/downloads/ 下载
- 安装到 `portable/python/` 目录
- 或使用系统已安装的Python

### 2. 安装依赖
首次运行会自动安装所有Python依赖包。

### 3. 下载AI模型
首次处理视频时会自动下载必要的AI模型。

### 4. 开始使用
1. 准备视频链接（抖音、快手等）
2. 准备用户人物图片
3. 运行程序开始复刻

## 配置说明

### 基本配置
编辑 `app/config_portable.json` 文件可以修改配置：

```json
{
  "app": {
    "name": "爆款视频复刻智能体",
    "debug": false
  },
  "models": {
    "face_detection": {
      "model_path": "../models/face_detection/det_10g.onnx"
    }
  }
}
```

### 环境变量
复制 `app/.env.example` 为 `app/.env` 并修改：

```
# API密钥（可选）
OPENAI_API_KEY=your_key_here

# 代理设置（可选）
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080
```

## 常见问题

### Q1: 找不到Python解释器
**A**: 请安装Python 3.8+到 `python/` 目录，或确保系统已安装Python。

### Q2: 依赖安装失败
**A**: 尝试使用国内镜像：
```bash
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 模型下载失败
**A**: 可以手动下载模型文件到 `models/` 目录。

### Q4: 程序运行缓慢
**A**: 
1. 确保有足够的内存（8GB+）
2. 使用SSD硬盘
3. 关闭其他大型程序

## 获取帮助

### 查看文档
查看 `docs/` 目录中的文档文件：
- `USER_GUIDE.md` - 详细用户指南
- `LAUNCH_GUIDE.md` - 启动指南
- `QUICK_START.md` - 快速开始

### 命令行帮助
```bash
# 查看所有命令
start.bat --help

# 查看具体命令帮助
start.bat cli --help
start.bat api --help
start.bat batch --help
```

### 查看日志