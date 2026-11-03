"""
部署脚本
用于打包、发布和部署项目
"""

import os
import sys
import shutil
import subprocess
import tempfile
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime
import argparse
import json

from loguru import logger


def setup_logging():
    """设置日志"""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )


def get_version():
    """获取版本号"""
    try:
        from config_loader import get_config
        config = get_config()
        return config.app_version
    except:
        return "1.0.0"


def get_build_info():
    """获取构建信息"""
    import platform
    import getpass
    
    return {
        "timestamp": datetime.now().isoformat(),
        "version": get_version(),
        "platform": platform.system(),
        "platform_version": platform.release(),
        "architecture": platform.machine(),
        "python_version": platform.python_version(),
        "user": getpass.getuser(),
        "hostname": platform.node()
    }


def clean_build():
    """清理构建目录"""
    logger.info("清理构建目录...")
    
    dirs_to_clean = ["build", "dist", "__pycache__"]
    files_to_clean = ["*.spec", "*.pyc", "*.pyo", "*.pyd"]
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            shutil.rmtree(dir_path)
            logger.debug(f"清理目录: {dir_path}")
    
    for pattern in files_to_clean:
        for file in Path(".").glob(pattern):
            try:
                file.unlink()
                logger.debug(f"清理文件: {file}")
            except:
                pass
    
    logger.info("构建目录清理完成 ✓")
    return True


def build_executable(onefile=True, windowed=False, debug=False):
    """构建可执行文件"""
    logger.info("构建可执行文件...")
    
    if not Path("main.py").exists():
        logger.error("主程序文件不存在: main.py")
        return False
    
    try:
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
        data_files = [
            ("src", "src"),
            ("config.py", "."),
            ("requirements.txt", "."),
            ("README.md", "."),
            ("USER_GUIDE.md", "."),
            ("INSTALL.md", "."),
            ("PROJECT_SUMMARY.md", ".")
        ]
        
        for src, dst in data_files:
            if Path(src).exists():
                cmd.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
        
        # 添加图标（如果有）
        icon_path = "assets/icon.ico"
        if Path(icon_path).exists():
            cmd.extend(["--icon", icon_path])
        
        # 名称
        cmd.extend(["--name", "VideoReplicationAgent"])
        
        # 隐藏控制台（仅Windows）
        if sys.platform == "win32" and windowed:
            cmd.append("--noconsole")
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("可执行文件构建完成 ✓")
            
            # 显示输出信息
            dist_dir = Path("dist")
            if dist_dir.exists():
                for item in dist_dir.iterdir():
                    if item.is_file():
                        size = item.stat().st_size / (1024 * 1024)  # MB
                        logger.info(f"生成文件: {item.name} ({size:.2f} MB)")
            
            return True
        else:
            logger.error(f"构建失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"构建可执行文件时出错: {e}")
        return False


def build_docker():
    """构建Docker镜像"""
    logger.info("构建Docker镜像...")
    
    if not Path("Dockerfile").exists():
        logger.error("Dockerfile不存在")
        return False
    
    try:
        version = get_version()
        tag = f"openclaw/video-replication-agent:{version}"
        
        cmd = ["docker", "build", "-t", tag, "."]
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Docker镜像构建完成: {tag} ✓")
            
            # 同时标记为latest
            latest_cmd = ["docker", "tag", tag, "openclaw/video-replication-agent:latest"]
            subprocess.run(latest_cmd, capture_output=True, text=True)
            logger.info("同时标记为: openclaw/video-replication-agent:latest")
            
            return True
        else:
            logger.error(f"Docker构建失败: {result.stderr}")
            return False
            
    except FileNotFoundError:
        logger.error("Docker未安装或未在PATH中")
        return False
    except Exception as e:
        logger.error(f"构建Docker镜像时出错: {e}")
        return False


def create_archive(format="zip"):
    """创建归档文件"""
    logger.info(f"创建{format.upper()}归档文件...")
    
    version = get_version()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"video_replication_agent_v{version}_{timestamp}"
    
    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 复制文件到临时目录
            files_to_copy = [
                "main.py", "run.py", "config.py", "requirements.txt",
                "README.md", "USER_GUIDE.md", "INSTALL.md", "PROJECT_SUMMARY.md",
                "start.sh", "start.bat", "Dockerfile", "docker-compose.yml",
                "nginx.conf", ".env.example"
            ]
            
            dirs_to_copy = [
                "src", "api", "web_admin", "examples", "tests", "utils", "monitor"
            ]
            
            # 复制文件
            for file in files_to_copy:
                src = Path(file)
                if src.exists():
                    dst = temp_path / file
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
            
            # 复制目录
            for dir_name in dirs_to_copy:
                src = Path(dir_name)
                if src.exists():
                    dst = temp_path / dir_name
                    shutil.copytree(src, dst, dirs_exist_ok=True)
            
            # 创建构建信息文件
            build_info = get_build_info()
            build_info_file = temp_path / "BUILD_INFO.json"
            with open(build_info_file, 'w', encoding='utf-8') as f:
                json.dump(build_info, f, indent=2, ensure_ascii=False)
            
            # 创建归档文件
            if format.lower() == "zip":
                archive_path = Path(f"{archive_name}.zip")
                with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in temp_path.rglob("*"):
                        if file_path.is_file():
                            arcname = file_path.relative_to(temp_path)
                            zipf.write(file_path, arcname)
            
            elif format.lower() == "tar.gz":
                archive_path = Path(f"{archive_name}.tar.gz")
                with tarfile.open(archive_path, 'w:gz') as tar:
                    tar.add(temp_path, arcname=archive_name)
            
            else:
                logger.error(f"不支持的归档格式: {format}")
                return False
            
            size = archive_path.stat().st_size / (1024 * 1024)  # MB
            logger.info(f"归档文件创建完成: {archive_path} ({size:.2f} MB) ✓")
            
            return True
            
    except Exception as e:
        logger.error(f"创建归档文件时出错: {e}")
        return False


def create_installer():
    """创建安装程序（Windows）"""
    if sys.platform != "win32":
        logger.warning("安装程序仅支持Windows系统")
        return False
    
    logger.info("创建安装程序...")
    
    try:
        # 检查Inno Setup
        result = subprocess.run(["iscc", "/?"], capture_output=True, text=True)
        if result.returncode != 0:
            logger.error("Inno Setup未安装或未在PATH中")
            return False
        
        # 创建ISS文件
        version = get_version()
        iss_content = f"""; 爆款视频复刻智能体 - Inno Setup脚本

#define MyAppName "爆款视频复刻智能体"
#define MyAppVersion "{version}"
#define MyAppPublisher "OpenClaw AI"
#define MyAppURL "https://openclaw.ai"
#define MyAppExeName "VideoReplicationAgent.exe"

[Setup]
AppId={{{{MyAppName}}}-{{MyAppVersion}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
AppPublisherURL={{#MyAppURL}}
AppSupportURL={{#MyAppURL}}
AppUpdatesURL={{#MyAppURL}}
DefaultDirName={{autopf}}\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
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
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked

[Files]
Source: "dist\\VideoReplicationAgent\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "models\\*"; DestDir: "{{app}}\\models"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\\*"; DestDir: "{{app}}\\data"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{{group}}\{{#MyAppName}}"; Filename: "{{app}}\{{#MyAppExeName}}"
Name: "{{group}}\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\{{#MyAppName}}"; Filename: "{{app}}\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

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
        
        iss_file = Path("installer.iss")
        with open(iss_file, 'w', encoding='utf-8') as f:
            f.write(iss_content)
        
        # 编译安装程序
        cmd = ["iscc", "installer.iss"]
        
        logger.info(f"执行命令: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info("安装程序创建完成 ✓")
            
            # 显示安装程序信息
            installer_dir = Path("installer")
            if installer_dir.exists():
                for file in installer_dir.glob("*.exe"):
                    size = file.stat().st_size / (1024 * 1024)  # MB
                    logger.info(f"安装程序: {file.name} ({size:.2f} MB)")
            
            return True
        else:
            logger.error(f"创建安装程序失败: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"创建安装程序时出错: {e}")
        return False


def deploy_to_server(host, username, password=None, key_file=None):
    """部署到服务器"""
    logger.info(f"部署到服务器: {host}")
    
    try:
        import paramiko
        
        # 创建SSH客户端
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # 连接服务器
        if key_file:
            ssh.connect(host, username=username, key_filename=key_file)
        elif password:
            ssh.connect(host, username=username, password=password)
        else:
            logger.error("需要密码或密钥文件")
            return False
        
        logger.info(f"已连接到服务器: {host}")
        
        # 创建部署目录
        version = get_version()
        deploy_dir = f"/opt/video_replication_agent_v{version}"
        
        commands = [
            f"sudo mkdir -p {deploy_dir}",
            f"sudo chown {username}:{username} {deploy_dir}",
            f"cd {deploy_dir}"
        ]
        
        for cmd in commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            if stdout.channel.recv_exit_status() != 0:
                logger.error(f"命令执行失败: {cmd}")
                logger.error(stderr.read().decode())
                return False
        
        # 使用SFTP上传文件
        sftp = ssh.open_sftp()
        
        # 上传当前目录的所有文件
        local_dir = Path(".")
        for item in local_dir.rglob("*"):
            if item.is_file() and not any(part.startswith('.') for part in item.parts):
                remote_path = f"{deploy_dir}/{item.relative_to(local_dir)}"
                
                # 创建远程目录
                remote_dir = os.path.dirname(remote_path)
                ssh.exec_command(f"mkdir -p {remote_dir}")
                
                # 上传文件
                sftp.put(str(item), remote_path)
                logger.debug(f"上传文件: {item} -> {remote_path}")
        
        sftp.close()
        
        # 创建服务文件
        service_content = f"""[Unit]
Description=爆款视频复刻智能体
After=network.target

[Service]
Type=simple
User={username}
WorkingDirectory={deploy_dir}
ExecStart={sys.executable} run.py service
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
        
        service_file = "/tmp/video_replication_agent.service"
        with open(service_file, 'w', encoding='utf-8') as f:
            f.write(service_content)
        
        # 上传服务文件
        sftp = ssh.open_sftp()
        sftp.put(service_file, "/tmp/video_replication_agent.service")
        sftp.close()
        
        # 安装服务
        install_commands = [
            "sudo mv /tmp/video_replication_agent.service /etc/systemd/system/",
            "sudo systemctl daemon-reload",
            "sudo systemctl enable video_replication_agent",
            "sudo systemctl start video_replication_agent"
        ]
        
        for cmd in install_commands:
            stdin, stdout, stderr = ssh.exec_command(cmd)
            if stdout.channel.recv_exit_status() != 0:
                logger.error(f"命令执行失败: {cmd}")
                logger.error(stderr.read().decode())
                return False
        
        ssh.close()
        
        logger.info(f"部署完成: {deploy_dir} ✓")
        logger.info(f"服务状态: sudo systemctl status video_replication_agent")
        
        return True
        
    except ImportError:
        logger.error("需要paramiko库: pip install paramiko")
        return False
    except Exception as e:
        logger.error(f"部署到服务器时出错: {e}")
        return False


def create_release_notes():
    """创建发布说明"""
    logger.info("创建发布说明...")
    
    version = get_version()
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    notes = f"""# 爆款视频复刻智能体 v{version}

发布日期: {timestamp}

## 新功能

1. **核心功能**
   - 视频下载：支持抖音、快手、TikTok等平台
   - 人脸替换：基于InsightFace的高质量人脸替换
   - 文案重写：集成免费大模型，支持多种风格
   - 视频编辑：字幕添加、音频处理、质量优化

2. **用户界面**
   - 图形界面：PyQt6开发的用户友好界面
   - 命令行