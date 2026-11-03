"""
创建简单的便携版
"""

import os
import shutil
import zipfile
from pathlib import Path
import json
from datetime import datetime


def create_simple_portable():
    """创建简单的便携版"""
    print("=" * 60)
    print("爆款视频复刻智能体 - 简单便携版创建工具")
    print("=" * 60)
    
    project_root = Path(__file__).parent
    portable_name = "VideoReplicationAgent_Portable"
    portable_dir = project_root / portable_name
    
    # 清理旧目录
    if portable_dir.exists():
        shutil.rmtree(portable_dir)
    
    portable_dir.mkdir(parents=True)
    
    print("\n1. 复制必要文件...")
    
    # 复制Python文件
    files_to_copy = [
        "run.py", "main.py", "config.py", "config_loader.py",
        "download_models.py", "init_project.py", ".env.example"
    ]
    
    for file_name in files_to_copy:
        src = project_root / file_name
        if src.exists():
            shutil.copy2(src, portable_dir / file_name)
            print(f"  复制: {file_name}")
    
    # 复制目录
    dirs_to_copy = ["src", "api", "web_admin", "utils", "scripts", "examples"]
    for dir_name in dirs_to_copy:
        src = project_root / dir_name
        if src.exists():
            shutil.copytree(src, portable_dir / dir_name, dirs_exist_ok=True)
            print(f"  复制目录: {dir_name}")
    
    # 复制文档
    print("\n2. 复制文档...")
    docs_files = [
        "README.md", "USER_GUIDE.md", "LAUNCH_GUIDE.md",
        "QUICK_START.md", "INSTALL.md", "PROJECT_SUMMARY.md"
    ]
    
    for file_name in docs_files:
        src = project_root / file_name
        if src.exists():
            shutil.copy2(src, portable_dir / file_name)
            print(f"  复制文档: {file_name}")
    
    # 创建启动脚本
    print("\n3. 创建启动脚本...")
    
    # Windows批处理脚本
    bat_content = """@echo off
REM 爆款视频复刻智能体 - 便携版启动脚本

echo.
echo ========================================
echo   爆款视频复刻智能体 - 便携版
echo ========================================
echo.

cd /d "%~dp0"

REM 检查Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python!
    echo.
    echo 请安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 检查依赖
if not exist "requirements_installed.flag" (
    echo 首次运行，安装依赖...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo. > "requirements_installed.flag"
    echo 依赖安装完成!
)

REM 运行程序
echo.
echo 启动应用程序...
echo.
python run.py %*

echo.
if "%1"=="" pause
"""
    
    # Linux/macOS Shell脚本
    sh_content = """#!/bin/bash
# 爆款视频复刻智能体 - 便携版启动脚本

echo ""
echo "========================================"
echo "   爆款视频复刻智能体 - 便携版"
echo "========================================"
echo ""

cd "$(dirname "$0")"

# 检查Python
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "错误: 未找到Python!"
    echo ""
    echo "请安装Python 3.8或更高版本"
    echo "下载地址: https://www.python.org/downloads/"
    echo ""
    exit 1
fi

# 使用python3或python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# 检查依赖
if [ ! -f "requirements_installed.flag" ]; then
    echo "首次运行，安装依赖..."
    $PYTHON_CMD -m pip install --upgrade pip
    $PYTHON_CMD -m pip install -r requirements.txt
    touch "requirements_installed.flag"
    echo "依赖安装完成!"
fi

# 运行程序
echo ""
echo "启动应用程序..."
echo ""
$PYTHON_CMD run.py "$@"

echo ""
"""
    
    # 写入脚本文件
    bat_file = portable_dir / "start.bat"
    with open(bat_file, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    sh_file = portable_dir / "start.sh"
    with open(sh_file, 'w', encoding='utf-8') as f:
        f.write(sh_content)
    
    sh_file.chmod(0o755)
    
    # 创建requirements.txt
    print("\n4. 创建依赖文件...")
    requirements_content = """# 核心依赖
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

# Web服务
fastapi>=0.104.0
uvicorn>=0.24.0

# 工具库
loguru>=0.7.0
psutil>=5.9.0
numpy>=1.24.0
pillow>=10.0.0
requests>=2.31.0
python-dotenv>=1.0.0
"""
    
    requirements_file = portable_dir / "requirements.txt"
    with open(requirements_file, 'w', encoding='utf-8') as f:
        f.write(requirements_content)
    
    # 创建说明文件
    print("\n5. 创建说明文件...")
    readme_content = f"""# 爆款视频复刻智能体 - 便携版

版本: 1.0.0
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 快速开始

### Windows用户
1. 确保已安装Python 3.8+
2. 双击运行 `start.bat`
3. 首次运行会自动安装依赖
4. 按照提示操作

### Linux/macOS用户
1. 确保已安装Python 3.8+
2. 打开终端
3. 运行: `chmod +x start.sh`
4. 运行: `./start.sh`
5. 首次运行会自动安装依赖

## 使用方法

### 图形界面模式
```
start.bat gui
```

### 命令行模式
```
start.bat cli --url "视频链接" --image "用户图片.jpg"
```

### API服务模式
```
start.bat api --port 8000
```

### 批量处理模式
```
start.bat batch --input "视频列表.txt" --images "图片目录/"
```

## 系统要求

- Python 3.8或更高版本
- 8GB RAM（推荐16GB）
- 20GB可用磁盘空间
- 网络连接（用于下载视频和模型）

## 获取帮助

- 查看 `USER_GUIDE.md` - 详细用户指南
- 查看 `LAUNCH_GUIDE.md` - 启动指南
- 查看 `QUICK_START.md` - 快速开始

运行 `start.bat --help` 查看所有命令选项。

---
祝您使用愉快！ 🎬✨
"""
    
    readme_file = portable_dir / "README_PORTABLE.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # 创建必要目录
    print("\n6. 创建必要目录...")
    for dir_name in ["data", "models", "logs", "temp"]:
        (portable_dir / dir_name).mkdir(exist_ok=True)
        print(f"  创建目录: {dir_name}")
    
    # 创建ZIP包
    print("\n7. 创建ZIP包...")
    zip_path = project_root / f"{portable_name}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in portable_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(portable_dir.parent)
                zipf.write(file_path, arcname)
    
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    
    # 显示结果
    print("\n" + "=" * 60)
    print("🎉 便携版创建完成!")
    print("=" * 60)
    
    print(f"\n📦 生成文件: {zip_path.name} ({size_mb:.1f} MB)")
    
    print("\n📁 包含内容:")
    print("  • 完整的Python源代码")
    print("  • 所有必要模块")
    print("  • 用户文档和指南")
    print("  • 启动脚本（Windows/Linux/macOS）")
    print("  • 配置文件示例")
    
    print("\n🚀 使用步骤:")
    print("  1. 解压ZIP包到任意目录")
    print("  2. 确保已安装Python 3.8+")
    print("  3. 运行 start.bat 或 start.sh")
    print("  4. 首次运行会自动安装依赖")
    print("  5. 按照提示开始使用")
    
    print("\n💡 提示:")
    print("  • 需要网络连接下载AI模型")
    print("  • 首次运行可能需要10-20分钟安装依赖")
    print("  • 查看文档获取详细指南")
    
    # 清理临时目录
    shutil.rmtree(portable_dir)
    
    print(f"\n✅ 完成！便携版已保存到: {zip_path}")
    return True


if __name__ == "__main__":
    create_simple_portable()