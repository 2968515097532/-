"""
项目初始化脚本
用于首次设置和配置项目
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse

from loguru import logger


def setup_logging():
    """设置日志"""
    from loguru import logger
    
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )


def check_requirements():
    """检查系统要求"""
    logger.info("检查系统要求...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error(f"需要Python 3.8或更高版本，当前版本: {python_version.major}.{python_version.minor}")
        return False
    
    logger.info(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro} ✓")
    
    # 检查操作系统
    import platform
    system = platform.system()
    logger.info(f"操作系统: {system} ✓")
    
    return True


def create_directory_structure():
    """创建目录结构"""
    logger.info("创建目录结构...")
    
    directories = [
        "data/input_videos",
        "data/output_videos",
        "data/user_images",
        "data/temp",
        "models/face_detection",
        "models/face_swap",
        "models/text",
        "logs",
        "backups",
        "web_admin/static",
        "web_admin/templates"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"创建目录: {path}")
    
    logger.info("目录结构创建完成 ✓")
    return True


def copy_config_files():
    """复制配置文件"""
    logger.info("复制配置文件...")
    
    config_files = {
        ".env.example": ".env",
        "config.example.json": "config.json",
        "config.example.yaml": "config.yaml"
    }
    
    for src, dst in config_files.items():
        src_path = Path(src)
        dst_path = Path(dst)
        
        if src_path.exists() and not dst_path.exists():
            shutil.copy2(src_path, dst_path)
            logger.debug(f"复制配置文件: {src} -> {dst}")
        elif dst_path.exists():
            logger.debug(f"配置文件已存在: {dst}")
        else:
            logger.warning(f"配置文件不存在: {src}")
    
    logger.info("配置文件复制完成 ✓")
    return True


def install_dependencies(use_mirror=False):
    """安装依赖"""
    logger.info("安装依赖包...")
    
    requirements_file = "requirements.txt"
    if not Path(requirements_file).exists():
        logger.error(f"依赖文件不存在: {requirements_file}")
        return False
    
    try:
        cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
        
        if use_mirror:
            # 使用国内镜像
            cmd.extend(["-i", "https://pypi.tuna.tsinghua.edu.cn/simple"])
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("依赖安装完成 ✓")
            return True
        else:
            logger.error(f"依赖安装失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"安装依赖时出错: {e}")
        return False


def download_models(force=False):
    """下载模型"""
    logger.info("下载模型文件...")
    
    try:
        from download_models import download_all_models
        
        success = download_all_models(force=force)
        
        if success:
            logger.info("模型下载完成 ✓")
            return True
        else:
            logger.error("模型下载失败")
            return False
            
    except ImportError:
        logger.error("无法导入模型下载模块")
        return False
    except Exception as e:
        logger.error(f"下载模型时出错: {e}")
        return False


def setup_environment_variables():
    """设置环境变量"""
    logger.info("设置环境变量...")
    
    # 检查.env文件
    env_file = Path(".env")
    if not env_file.exists():
        logger.warning(".env文件不存在，将使用默认配置")
        return True
    
    try:
        # 加载环境变量
        from dotenv import load_dotenv
        load_dotenv(env_file)
        
        logger.info("环境变量加载完成 ✓")
        return True
        
    except ImportError:
        logger.warning("未安装python-dotenv，跳过环境变量设置")
        return True
    except Exception as e:
        logger.error(f"加载环境变量时出错: {e}")
        return False


def run_tests():
    """运行测试"""
    logger.info("运行测试...")
    
    try:
        cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("测试通过 ✓")
            return True
        else:
            logger.error(f"测试失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"运行测试时出错: {e}")
        return False


def create_startup_scripts():
    """创建启动脚本"""
    logger.info("创建启动脚本...")
    
    scripts = {
        "start.sh": """#!/bin/bash
# 爆款视频复刻智能体 - 启动脚本

cd "$(dirname "$0")"

# 激活虚拟环境（如果存在）
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# 运行应用
python run.py "$@"
""",
        
        "start.bat": """@echo off
REM 爆款视频复刻智能体 - Windows启动脚本

cd /d "%~dp0"

REM 激活虚拟环境（如果存在）
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM 运行应用
python run.py %*
"""
    }
    
    for filename, content in scripts.items():
        path = Path(filename)
        
        if not path.exists():
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 设置执行权限（Linux/macOS）
            if filename.endswith('.sh'):
                path.chmod(0o755)
            
            logger.debug(f"创建启动脚本: {filename}")
    
    logger.info("启动脚本创建完成 ✓")
    return True


def create_virtual_environment():
    """创建虚拟环境"""
    logger.info("创建虚拟环境...")
    
    venv_dir = Path("venv")
    if venv_dir.exists():
        logger.info("虚拟环境已存在，跳过创建")
        return True
    
    try:
        cmd = [sys.executable, "-m", "venv", "venv"]
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("虚拟环境创建完成 ✓")
            
            # 在虚拟环境中安装pip
            if sys.platform == "win32":
                pip_cmd = ["venv\\Scripts\\python", "-m", "pip", "install", "--upgrade", "pip"]
            else:
                pip_cmd = ["venv/bin/python", "-m", "pip", "install", "--upgrade", "pip"]
            
            subprocess.run(pip_cmd, capture_output=True, text=True)
            
            return True
        else:
            logger.error(f"创建虚拟环境失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"创建虚拟环境时出错: {e}")
        return False


def generate_config_summary():
    """生成配置摘要"""
    logger.info("生成配置摘要...")
    
    try:
        from config_loader import init_config
        config = init_config()
        config.print_summary()
        return True
    except Exception as e:
        logger.error(f"生成配置摘要时出错: {e}")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="爆款视频复刻智能体 - 项目初始化")
    parser.add_argument("--skip-deps", action="store_true", help="跳过依赖安装")
    parser.add_argument("--skip-models", action="store_true", help="跳过模型下载")
    parser.add_argument("--skip-tests", action="store_true", help="跳过测试")
    parser.add_argument("--force-models", action="store_true", help="强制重新下载模型")
    parser.add_argument("--use-mirror", action="store_true", help="使用国内镜像")
    parser.add_argument("--create-venv", action="store_true", help="创建虚拟环境")
    parser.add_argument("--quick", action="store_true", help="快速模式（跳过测试）")
    
    args = parser.parse_args()
    
    # 设置日志
    setup_logging()
    
    print("=" * 60)
    print("爆款视频复刻智能体 - 项目初始化")
    print("=" * 60)
    
    # 检查系统要求
    if not check_requirements():
        sys.exit(1)
    
    # 创建目录结构
    if not create_directory_structure():
        sys.exit(1)
    
    # 复制配置文件
    if not copy_config_files():
        sys.exit(1)
    
    # 创建虚拟环境（可选）
    if args.create_venv:
        if not create_virtual_environment():
            sys.exit(1)
    
    # 安装依赖
    if not args.skip_deps:
        if not install_dependencies(args.use_mirror):
            sys.exit(1)
    
    # 下载模型
    if not args.skip_models:
        if not download_models(args.force_models):
            sys.exit(1)
    
    # 设置环境变量
    if not setup_environment_variables():
        sys.exit(1)
    
    # 运行测试
    if not args.skip_tests and not args.quick:
        if not run_tests():
            logger.warning("测试失败，但继续初始化")
    
    # 创建启动脚本
    if not create_startup_scripts():
        sys.exit(1)
    
    # 生成配置摘要
    if not generate_config_summary():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("项目初始化完成!")
    print("=" * 60)
    
    print("\n下一步:")
    print("1. 编辑 .env 文件配置环境变量")
    print("2. 编辑 config.json 或 config.yaml 文件配置应用")
    print("3. 运行测试: python -m pytest tests/ -v")
    print("4. 启动应用:")
    print("   - 命令行: python run.py cli --url 视频链接 --image 用户图片")
    print("   - GUI界面: python run.py gui")
    print("   - API服务: python run.py api")
    print("   - 管理面板: python run.py admin")
    print("\n快速开始:")
    print("  ./start.sh --help  # Linux/macOS")
    print("  start.bat --help   # Windows")
    
    print("\n文档:")
    print("  - 用户指南: cat USER_GUIDE.md")
    print("  - 安装指南: cat INSTALL.md")
    print("  - 项目总结: cat PROJECT_SUMMARY.md")
    
    print("\n技术支持:")
    print("  - GitHub: https://github.com/openclaw/video-replication-agent")
    print("  - Discord: https://discord.gg/clawd")
    
    print("\n祝您使用愉快! 🎬✨")


if __name__ == "__main__":
    main()