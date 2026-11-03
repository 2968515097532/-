"""
构建脚本
用于打包成可执行文件
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse


def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ["build", "dist", "__pycache__", "*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            if os.path.isdir(dir_name):
                shutil.rmtree(dir_name)
                print(f"已清理目录: {dir_name}")
            else:
                # 处理通配符
                for spec_file in Path(".").glob(dir_name):
                    spec_file.unlink()
                    print(f"已删除文件: {spec_file}")


def install_dependencies():
    """安装依赖"""
    print("正在安装依赖...")
    
    try:
        # 安装requirements.txt中的依赖
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"依赖安装失败: {e}")
        return False
    
    return True


def build_executable(onefile=True, windowed=False, debug=False):
    """构建可执行文件"""
    print("正在构建可执行文件...")
    
    # PyInstaller命令
    cmd = [sys.executable, "-m", "PyInstaller"]
    
    # 主程序文件
    cmd.append("main.py")
    
    # 添加参数
    if onefile:
        cmd.append("--onefile")
    
    if windowed:
        cmd.append("--windowed")
    
    if debug:
        cmd.append("--debug")
    
    # 添加数据文件
    cmd.extend([
        "--add-data", "src;src",
        "--add-data", "config.py;.",
        "--add-data", "requirements.txt;.",
        "--add-data", "README.md;.",
    ])
    
    # 添加图标（如果有）
    icon_path = "assets/icon.ico"
    if os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # 名称
    cmd.extend(["--name", "VideoReplicationAgent"])
    
    # 隐藏控制台（仅Windows）
    if sys.platform == "win32" and windowed:
        cmd.append("--noconsole")
    
    print(f"执行命令: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("构建完成!")
        
        # 显示输出信息
        dist_dir = "dist"
        if os.path.exists(dist_dir):
            for file in os.listdir(dist_dir):
                file_path = os.path.join(dist_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    print(f"生成文件: {file} ({size:.2f} MB)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        return False


def build_docker():
    """构建Docker镜像"""
    print("正在构建Docker镜像...")
    
    # 检查Dockerfile是否存在
    if not os.path.exists("Dockerfile"):
        print("错误: Dockerfile不存在")
        return False
    
    try:
        # 构建Docker镜像
        subprocess.check_call([
            "docker", "build",
            "-t", "video-replication-agent:latest",
            "."
        ])
        print("Docker镜像构建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Docker构建失败: {e}")
        return False
    except FileNotFoundError:
        print("错误: Docker未安装或未在PATH中")
        return False


def create_installer():
    """创建安装程序（Windows）"""
    if sys.platform != "win32":
        print("警告: 安装程序仅支持Windows系统")
        return False
    
    print("正在创建安装程序...")
    
    # 使用Inno Setup创建安装程序
    iss_template = """#define MyAppName "爆款视频复刻智能体"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "OpenClaw AI"
#define MyAppURL "https://openclaw.ai"
#define MyAppExeName "VideoReplicationAgent.exe"

[Setup]
AppId={{{{{MyAppName}}}-{MyAppVersion}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={{autopf}}\\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=VideoReplicationAgent_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "chinese"; MessagesFile: "compiler:Languages\\Chinese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\VideoReplicationAgent\\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "models\\*"; DestDir: "{app}\\models"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\\*"; DestDir: "{app}\\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"
Name: "{group}\\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\{#MyAppName}"; Filename: "{app}\\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  // 检查Python是否安装
  if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.8\\InstallPath') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.9\\InstallPath') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.10\\InstallPath') and
     not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python\\PythonCore\\3.11\\InstallPath') then
  begin
    if MsgBox('未检测到Python 3.8+，是否继续安装？', mbConfirmation, MB_YESNO) = IDNO then
      Result := False;
  end;
end;
"""
    
    # 写入ISS文件
    with open("installer.iss", "w", encoding="utf-8") as f:
        f.write(iss_template)
    
    try:
        # 编译安装程序
        subprocess.check_call([
            "iscc", "installer.iss"
        ])
        
        print("安装程序创建完成")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"安装程序创建失败: {e}")
        return False
    except FileNotFoundError:
        print("错误: Inno Setup未安装或未在PATH中")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="爆款视频复刻智能体构建工具")
    parser.add_argument("--clean", action="store_true", help="清理构建目录")
    parser.add_argument("--install", action="store_true", help="安装依赖")
    parser.add_argument("--build", action="store_true", help="构建可执行文件")
    parser.add_argument("--docker", action="store_true", help="构建Docker镜像")
    parser.add_argument("--installer", action="store_true", help="创建安装程序（Windows）")
    parser.add_argument("--all", action="store_true", help="执行所有构建步骤")
    parser.add_argument("--onefile", action="store_true", default=True, help="打包为单个文件")
    parser.add_argument("--windowed", action="store_true", help="无控制台窗口（GUI模式）")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    # 如果没有指定任何操作，显示帮助
    if not any([args.clean, args.install, args.build, args.docker, args.installer, args.all]):
        parser.print_help()
        return
    
    # 执行所有步骤
    if args.all:
        args.clean = True
        args.install = True
        args.build = True
    
    # 清理
    if args.clean:
        clean_build_dirs()
    
    # 安装依赖
    if args.install:
        if not install_dependencies():
            return
    
    # 构建可执行文件
    if args.build:
        if not build_executable(args.onefile, args.windowed, args.debug):
            return
    
    # 构建Docker镜像
    if args.docker:
        build_docker()
    
    # 创建安装程序
    if args.installer:
        create_installer()
    
    print("\n构建完成!")
    
    # 显示使用说明
    if args.build:
        print("\n使用说明:")
        print("1. 命令行模式: dist/VideoReplicationAgent.exe --url 视频链接 --image 用户图片")
        print("2. GUI模式: dist/VideoReplicationAgent.exe --gui")
        print("3. API模式: dist/VideoReplicationAgent.exe --api --port 8000")


if __name__ == "__main__":
    main()