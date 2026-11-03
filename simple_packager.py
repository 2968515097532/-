"""
简单打包脚本 - 不依赖外部库
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import zipfile


def clean_build():
    """清理构建目录"""
    print("清理构建目录...")
    
    project_root = Path(__file__).parent
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        dir_path = project_root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path, ignore_errors=True)
            print(f"清理目录: {dir_path}")
    
    # 清理spec文件
    for spec_file in project_root.glob("*.spec"):
        try:
            spec_file.unlink()
            print(f"清理文件: {spec_file}")
        except:
            pass
    
    print("构建目录清理完成")
    return True


def build_executable():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    project_root = Path(__file__).parent
    
    # 确定主程序文件
    main_script = project_root / "run.py"
    if not main_script.exists():
        main_script = project_root / "main.py"
    
    if not main_script.exists():
        print("错误: 找不到主程序文件")
        return False
    
    try:
        # 使用PyInstaller构建
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--name=VideoReplicationAgent",
            "--clean",
            "--noconfirm",
            "--add-data=src;src",
            "--add-data=config.py;.",
            "--add-data=config_loader.py;.",
            "--add-data=README.md;.",
            "--add-data=USER_GUIDE.md;.",
            "--add-data=LAUNCH_GUIDE.md;.",
            "--hidden-import=torch",
            "--hidden-import=torchvision",
            "--hidden-import=opencv_python",
            "--hidden-import=moviepy",
            "--hidden-import=insightface",
            "--hidden-import=transformers",
            "--hidden-import=PyQt6",
            "--hidden-import=fastapi",
            str(main_script)
        ]
        
        print(f"执行构建命令: {' '.join(cmd)}")
        
        # 运行构建
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("可执行文件构建成功!")
            
            # 显示构建结果
            dist_dir = project_root / "dist"
            exe_path = dist_dir / "VideoReplicationAgent.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"生成可执行文件: {exe_path} ({size_mb:.2f} MB)")
                
                # 测试运行
                test_executable(exe_path)
                
                return True
            else:
                print("错误: 可执行文件未生成")
                return False
        else:
            print(f"构建失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"构建过程中出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_executable(exe_path):
    """测试可执行文件"""
    print("测试可执行文件...")
    
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
            print("可执行文件测试通过")
            return True
        else:
            print(f"可执行文件返回非零状态码: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("可执行文件测试超时")
        return False
    except Exception as e:
        print(f"测试可执行文件时出错: {e}")
        return False


def create_complete_package():
    """创建完整包"""
    print("创建完整包...")
    
    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    
    # 首先构建可执行文件
    if not build_executable():
        return False
    
    # 创建完整包目录
    package_name = "VideoReplicationAgent_Complete"
    package_dir = dist_dir / package_name
    package_dir.mkdir(exist_ok=True)
    
    try:
        # 复制可执行文件
        exe_src = dist_dir / "VideoReplicationAgent.exe"
        if exe_src.exists():
            shutil.copy2(exe_src, package_dir / "VideoReplicationAgent.exe")
            print(f"复制可执行文件: {exe_src.name}")
        
        # 创建启动脚本
        create_launch_scripts(package_dir)
        
        # 复制必要文件
        copy_essential_files(project_root, package_dir)
        
        # 创建必要目录
        create_necessary_directories(package_dir)
        
        # 创建说明文件
        create_readme_file(package_dir)
        
        # 创建ZIP包
        zip_path = dist_dir / f"{package_name}.zip"
        create_zip_package(package_dir, zip_path)
        
        # 显示结果
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"完整包创建完成: {zip_path} ({size_mb:.1f} MB)")
        
        show_final_results(dist_dir, package_name, size_mb)
        
        return True
        
    except Exception as e:
        print(f"创建完整包失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_launch_scripts(package_dir):
    """创建启动脚本"""
    # Windows批处理脚本
    bat_content = """@echo off
REM 爆款视频复刻智能体 - Windows启动脚本

echo ========================================
echo   爆款视频复刻智能体
echo ========================================
echo.

if exist "VideoReplicationAgent.exe" (
    echo 启动应用程序...
    VideoReplicationAgent.exe %*
) else (
    echo 错误: 找不到可执行文件!
    pause
    exit /b 1
)

echo.
if "%1"=="" pause
"""
    
    # Linux/macOS Shell脚本
    sh_content = """#!/bin/bash
# 爆款视频复刻智能体 - Linux/macOS启动脚本

echo "========================================"
echo "   爆款视频复刻智能体"
echo "========================================"
echo ""

if [ -f "VideoReplicationAgent" ]; then
    echo "启动应用程序..."
    ./VideoReplicationAgent "$@"
elif [ -f "VideoReplicationAgent.exe" ]; then
    echo "启动应用程序..."
    ./VideoReplicationAgent.exe "$@"
else
    echo "错误: 找不到可执行文件!"
    exit 1
fi

echo ""
"""
    
    # 写入脚本文件
    bat_file = package_dir / "start.bat"
    with open(bat_file, 'w', encoding='utf-8') as f:
        f.write(bat_content)
    
    sh_file = package_dir / "start.sh"
    with open(sh_file, 'w', encoding='utf-8') as f:
        f.write(sh_content)
    
    # 设置执行权限
    sh_file.chmod(0o755)
    
    print("启动脚本创建完成")


def copy_essential_files(project_root, package_dir):
    """复制必要文件"""
    essential_files = [
        "README.md", "USER_GUIDE.md", "LAUNCH_GUIDE.md",
        "QUICK_START.md", "INSTALL.md", "PROJECT_SUMMARY.md",
        "config.py", "config_loader.py", ".env.example"
    ]
    
    for file_name in essential_files:
        file_src = project_root / file_name
        if file_src.exists():
            shutil.copy2(file_src, package_dir / file_name)
            print(f"复制文件: {file_name}")


def create_necessary_directories(package_dir):
    """创建必要目录"""
    for dir_name in ["data", "models", "logs", "temp"]:
        dir_path = package_dir / dir_name
        dir_path.mkdir(exist_ok=True)
        print(f"创建目录: {dir_name}")


def create_readme_file(package_dir):
    """创建说明文件"""
    readme_content = """# 爆款视频复刻智能体 - 完整包

## 使用说明

### Windows用户
1. 解压此ZIP包到任意目录
2. 双击运行 `start.bat`
3. 或直接运行 `VideoReplicationAgent.exe`

### Linux/macOS用户
1. 解压此ZIP包到任意目录
2. 打开终端
3. 运行: `chmod +x start.sh`
4. 运行: `./start.sh`

## 首次使用

1. 复制 `.env.example` 为 `.env`
2. 根据需要修改配置
3. 运行程序，它会自动下载必要的AI模型
4. 按照提示操作

## 功能特点

- ✅ 视频下载（抖音、快手、TikTok等）
- ✅ 人脸检测和替换
- ✅ 文案自动重写
- ✅ 视频编辑和优化
- ✅ 图形界面和命令行
- ✅ 批量处理支持

## 系统要求

- 操作系统: Windows 10/11, Linux, macOS
- 内存: 至少8GB RAM
- 存储: 至少20GB可用空间
- Python: 已包含在包中，无需单独安装

## 获取帮助

查看包内的文档文件获取详细指南:
- `USER_GUIDE.md` - 用户指南
- `LAUNCH_GUIDE.md` - 启动指南
- `QUICK_START.md` - 快速开始

---
祝您使用愉快！ 🎬✨
"""
    
    readme_file = package_dir / "README_COMPLETE.md"
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("说明文件创建完成")


def create_zip_package(package_dir, zip_path):
    """创建ZIP包"""
    print("创建ZIP包...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"ZIP包创建完成: {zip_path}")


def show_final_results(dist_dir, package_name, size_mb):
    """显示最终结果"""
    print("\n" + "=" * 60)
    print("🎉 打包完成!")
    print("=" * 60)
    
    print(f"\n📦 生成的文件:")
    print(f"  1. 可执行文件: {dist_dir}/VideoReplicationAgent.exe")
    print(f"  2. 完整包: {dist_dir}/{package_name}.zip ({size_mb:.1f} MB)")
    print(f"  3. 启动脚本: {dist_dir}/{package_name}/start.bat")
    print(f"  4. 启动脚本: {dist_dir}/{package_name}/start.sh")
    
    print("\n🚀 使用方法:")
    print("  1. 解压完整包到任意目录")
    print("  2. 运行 start.bat (Windows) 或 start.sh (Linux/macOS)")
    print("  3. 首次运行会自动下载AI模型")
    print("  4. 按照提示输入视频链接和用户图片")
    
    print("\n💡 提示:")
    print("  • 确保有足够的磁盘空间（至少2GB）")
    print("  • 首次运行需要网络连接下载模型")
    print("  • 查看 USER_GUIDE.md 获取详细指南")
    print("  • 查看 LAUNCH_GUIDE.md 获取启动指南")


def main():
    """主函数"""
    print("爆款视频复刻智能体 - 打包工具")
    print("=" * 40)
    
    try:
        # 清理构建目录
        clean_build()
        
        # 创建完整包
        success = create_complete_package()
        
        if success:
            print("\n🎉 打包成功！")
            print("应用程序已准备好分发。")
        else:
            print("\n❌ 打包失败")
            print("请检查错误信息。")
        
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"打包失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()