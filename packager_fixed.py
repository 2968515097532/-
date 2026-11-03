"""
可执行程序打包脚本 - 修复版
使用PyInstaller打包完整的应用程序
"""

import os
import sys
import shutil
import subprocess
import tempfile
import json
from pathlib import Path
import argparse
from datetime import datetime

from loguru import logger


class AppPackager:
    """应用程序打包器"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.spec_dir = self.project_root
        
    def clean_build(self):
        """清理构建目录"""
        logger.info("清理构建目录...")
        
        dirs_to_clean = ["build", "dist", "__pycache__"]
        files_to_clean = ["*.spec", "*.pyc", "*.pyo", "*.pyd"]
        
        for dir_name in dirs_to_clean:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                shutil.rmtree(dir_path)
                logger.debug(f"清理目录: {dir_path}")
        
        for pattern in files_to_clean:
            for file in self.project_root.glob(pattern):
                try:
                    file.unlink()
                    logger.debug(f"清理文件: {file}")
                except:
                    pass
        
        # 清理子目录中的__pycache__
        for pycache in self.project_root.rglob("__pycache__"):
            try:
                shutil.rmtree(pycache)
                logger.debug(f"清理目录: {pycache}")
            except:
                pass
        
        logger.info("构建目录清理完成")
        return True
    
    def check_dependencies(self):
        """检查依赖"""
        logger.info("检查打包依赖...")
        
        required_packages = ["pyinstaller", "setuptools"]
        missing = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            logger.error(f"缺少依赖包: {', '.join(missing)}")
            logger.info(f"请运行: pip install {' '.join(missing)}")
            return False
        
        logger.info("所有依赖包已安装")
        return True
    
    def build_simple_executable(self):
        """构建简单的可执行文件"""
        logger.info("开始构建简单的可执行文件...")
        
        # 清理构建目录
        self.clean_build()
        
        # 确定主程序文件
        main_script = self.project_root / "run.py"
        if not main_script.exists():
            main_script = self.project_root / "main.py"
        
        if not main_script.exists():
            logger.error("找不到主程序文件")
            return False
        
        try:
            # 使用PyInstaller构建
            cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--name=VideoReplicationAgent",
                "--clean",
                "--noconfirm",
                str(main_script)
            ]
            
            logger.info(f"执行构建命令: {' '.join(cmd)}")
            
            # 运行构建
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                logger.info("可执行文件构建成功!")
                
                # 显示构建结果
                exe_path = self.dist_dir / "VideoReplicationAgent.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    logger.info(f"生成可执行文件: {exe_path} ({size_mb:.2f} MB)")
                    
                    # 测试运行
                    self._test_simple_executable(exe_path)
                    
                    # 创建启动脚本
                    self._create_simple_launch_scripts()
                    
                    return True
                else:
                    logger.error("可执行文件未生成")
                    return False
            else:
                logger.error(f"构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"构建过程中出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _test_simple_executable(self, exe_path):
        """测试可执行文件"""
        logger.info("测试可执行文件...")
        
        try:
            # 运行帮助命令
            cmd = [str(exe_path), "--help"]
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logger.info("可执行文件测试通过")
                return True
            else:
                logger.warning(f"可执行文件返回非零状态码: {result.returncode}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.warning("可执行文件测试超时")
            return False
        except Exception as e:
            logger.warning(f"测试可执行文件时出错: {e}")
            return False
    
    def _create_simple_launch_scripts(self):
        """创建启动脚本"""
        logger.info("创建启动脚本...")
        
        # Windows批处理脚本
        bat_content = """@echo off
REM 爆款视频复刻智能体 - Windows启动脚本
REM 版本: 1.0.0

echo ========================================
echo   爆款视频复刻智能体
echo ========================================
echo.

REM 设置环境变量
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

REM 运行程序
if exist "VideoReplicationAgent.exe" (
    echo 启动可执行文件...
    VideoReplicationAgent.exe %*
) else (
    echo 错误: 找不到可执行文件!
    pause
    exit /b 1
)

echo.
echo 程序执行完成。
if "%1"=="" pause
"""
        
        # Linux/macOS Shell脚本
        sh_content = """#!/bin/bash
# 爆款视频复刻智能体 - Linux/macOS启动脚本
# 版本: 1.0.0

echo "========================================"
echo "   爆款视频复刻智能体"
echo "========================================"
echo ""

# 设置环境变量
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1

# 运行程序
if [ -f "VideoReplicationAgent" ]; then
    echo "启动可执行文件..."
    ./VideoReplicationAgent "$@"
elif [ -f "VideoReplicationAgent.exe" ]; then
    echo "启动可执行文件..."
    ./VideoReplicationAgent.exe "$@"
else
    echo "错误: 找不到可执行文件!"
    exit 1
fi

echo ""
echo "程序执行完成。"
"""
        
        # 写入脚本文件
        bat_file = self.dist_dir / "start.bat"
        with open(bat_file, 'w', encoding='utf-8') as f:
            f.write(bat_content)
        
        sh_file = self.dist_dir / "start.sh"
        with open(sh_file, 'w', encoding='utf-8') as f:
            f.write(sh_content)
        
        # 设置执行权限
        sh_file.chmod(0o755)
        
        logger.info(f"启动脚本创建完成: {bat_file}, {sh_file}")
    
    def create_complete_package(self):
        """创建完整包（包含数据文件）"""
        logger.info("创建完整包...")
        
        # 首先构建可执行文件
        if not self.build_simple_executable():
            return False
        
        # 创建完整包目录
        package_name = "VideoReplicationAgent_Complete"
        package_dir = self.dist_dir / package_name
        package_dir.mkdir(exist_ok=True)
        
        try:
            # 复制可执行文件
            exe_src = self.dist_dir / "VideoReplicationAgent.exe"
            if exe_src.exists():
                shutil.copy2(exe_src, package_dir / "VideoReplicationAgent.exe")
            
            # 复制启动脚本
            for script in ["start.bat", "start.sh"]:
                script_src = self.dist_dir / script
                if script_src.exists():
                    shutil.copy2(script_src, package_dir / script)
            
            # 复制必要文件
            essential_files = [
                "README.md", "USER_GUIDE.md", "LAUNCH_GUIDE.md",
                "QUICK_START.md", "INSTALL.md", "PROJECT_SUMMARY.md"
            ]
            
            for file_name in essential_files:
                file_src = self.project_root / file_name
                if file_src.exists():
                    shutil.copy2(file_src, package_dir / file_name)
            
            # 复制配置文件示例
            config_example = self.project_root / ".env.example"
            if config_example.exists():
                shutil.copy2(config_example, package_dir / ".env.example")
            
            # 创建必要目录
            for dir_name in ["data", "models", "logs", "temp"]:
                (package_dir / dir_name).mkdir(exist_ok=True)
            
            # 创建说明文件
            readme_content = """# 爆款视频复刻智能体 - 完整包

## 包含内容

1. **可执行文件**: VideoReplicationAgent.exe
2. **启动脚本**: start.bat (Windows), start.sh (Linux/macOS)
3. **用户文档**: 各种使用指南和说明
4. **配置文件示例**: .env.example
5. **必要目录**: data/, models/, logs/, temp/

## 使用说明

### Windows用户
1. 双击运行 `start.bat`
2. 或直接运行 `VideoReplicationAgent.exe`

### Linux/macOS用户
1. 打开终端
2. 运行: `chmod +x start.sh`
3. 运行: `./start.sh`

## 首次使用

1. 复制 `.env.example` 为 `.env`
2. 根据需要修改配置
3. 将模型文件放入 `models/` 目录
4. 运行程序开始使用

## 获取帮助

- 查看 `USER_GUIDE.md` 获取详细使用指南
- 查看 `LAUNCH_GUIDE.md` 获取启动指南
- 查看 `QUICK_START.md` 获取快速开始指南

---
祝您使用愉快！ 🎬✨
"""
            
            readme_file = package_dir / "README_COMPLETE.md"
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # 创建ZIP包
            import zipfile
            zip_path = self.dist_dir / f"{package_name}.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(package_dir)
                        zipf.write(file_path, arcname)
            
            # 显示结果
            size_mb = zip_path.stat().st_size / (1024 * 1024)
            logger.info(f"完整包创建完成: {zip_path} ({size_mb:.1f} MB)")
            
            print("\n" + "=" * 60)
            print("打包完成!")
            print("=" * 60)
            print(f"\n📦 生成的文件:")
            print(f"  1. 可执行文件: dist/VideoReplicationAgent.exe")
            print(f"  2. 完整包: dist/{package_name}.zip")
            print(f"  3. 启动脚本: dist/start.bat, dist/start.sh")
            
            print("\n🚀 使用方法:")
            print("  1. 解压完整包到任意目录")
            print("  2. 运行 start.bat (Windows) 或 start.sh (Linux/macOS)")
            print("  3. 按照提示操作")
            
            print("\n💡 提示:")
            print("  • 首次运行需要下载AI模型")
            print("  • 确保有足够的磁盘空间（至少2GB）")
            print("  • 查看 USER_GUIDE.md 获取详细指南")
            
            return True
            
        except Exception as e:
            logger.error(f"创建完整包失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="爆款视频复刻智能体 - 简单打包工具")
    parser.add_argument("--clean", action="store_true", help="清理构建目录")
    parser.add_argument("--simple", action="store_true", help="构建简单可执行文件")
    parser.add_argument("--complete", action="store_true", help="构建完整包")
    parser.add_argument("--all", action="store_true", help="执行完整打包")
    
    args = parser.parse_args()
    
    # 设置日志
    from loguru import logger
    logger.remove()
    logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
    
    packager = AppPackager()
    
    try:
        if args.clean:
            packager.clean_build()
            print("清理完成")
            return
        
        if args.all or args.complete:
            # 构建完整包
            success = packager.create_complete_package()
        elif args.simple:
            # 构建简单可执行文件
            success = packager.build_simple_executable()
        else:
            # 默认构建完整包
            success = packager.create_complete_package()
        
        if success:
            print("\n🎉 打包成功！")
            print("应用程序已准备好分发。")
        else:
            print("\n❌ 打包失败")
            print("请检查错误信息并重试。")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        logger.error(f"打包失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()