        try:
            # 检查Inno Setup
            result = subprocess.run(["iscc", "/?"], capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("Inno Setup未安装或未在PATH中")
                logger.info("请从 https://jrsoftware.org/isinfo.php 下载安装Inno Setup")
                return None
            
            version = self._get_version()
            
            # 创建ISS脚本
            iss_content = self._generate_iss_script(version)
            
            iss_file = self.project_root / "installer.iss"
            with open(iss_file, 'w', encoding='utf-8') as f:
                f.write(iss_content)
            
            # 编译安装程序
            cmd = ["iscc", str(iss_file)]
            logger.info(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # 查找生成的安装程序
                installer_dir = self.project_root / "installer"
                if installer_dir.exists():
                    for file in installer_dir.glob("*.exe"):
                        size_mb = file.stat().st_size / (1024 * 1024)
                        logger.info(f"安装程序创建完成: {file.name} ({size_mb:.1f} MB)")
                        return str(file)
            
            logger.error(f"创建安装程序失败: {result.stderr}")
            return None
            
        except FileNotFoundError:
            logger.error("Inno Setup未安装或未在PATH中")
            return None
        except Exception as e:
            logger.error(f"创建Windows安装程序失败: {e}")
            return None
    
    def _generate_iss_script(self, version):
        """生成Inno Setup脚本"""
        return f"""; 爆款视频复刻智能体 - Inno Setup安装脚本
; 自动生成于: {datetime.now().isoformat()}

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
OutputBaseFilename=VideoReplicationAgent_Setup_v{version}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
SetupIconFile=assets/icon.ico
UninstallDisplayIcon={{app}}\{{#MyAppExeName}}
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

[Languages]
Name: "chinese"; MessagesFile: "compiler:Languages\\Chinese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{{cm:CreateQuickLaunchIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "dist\\VideoReplicationAgent\\*"; DestDir: "{{app}}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "models\\*"; DestDir: "{{app}}\\models"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "data\\*"; DestDir: "{{app}}\\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "examples\\*"; DestDir: "{{app}}\\examples"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "docs\\*"; DestDir: "{{app}}\\docs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "README.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "USER_GUIDE.md"; DestDir: "{{app}}"; Flags: ignoreversion
Source: "LAUNCH_GUIDE.md"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\{{#MyAppName}}"; Filename: "{{app}}\{{#MyAppExeName}}"
Name: "{{group}}\{{cm:UninstallProgram,{{#MyAppName}}}}"; Filename: "{{uninstallexe}}"
Name: "{{autodesktop}}\{{#MyAppName}}"; Filename: "{{app}}\{{#MyAppExeName}}"; Tasks: desktopicon
Name: "{{userappdata}}\Microsoft\\Internet Explorer\\Quick Launch\\{{#MyAppName}}"; Filename: "{{app}}\{{#MyAppExeName}}"; Tasks: quicklaunchicon

[Run]
Filename: "{{app}}\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName, '&', '&&')}}}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{{app}}\\logs"
Type: filesandordirs; Name: "{{app}}\\temp"
Type: filesandordirs; Name: "{{app}}\\backups"

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  
  // 检查必要的运行时
  if not FileExists(ExpandConstant('{{sys}}\\vcruntime140.dll')) and
     not FileExists(ExpandConstant('{{sys}}\\vcruntime140_1.dll')) then
  begin
    if MsgBox('未检测到Visual C++ Redistributable，是否继续安装？' + #13#10 +
              '程序可能需要VC++运行时才能正常运行。',
              mbConfirmation, MB_YESNO) = IDNO then
      Result := False;
  end;
  
  // 检查磁盘空间（至少需要2GB）
  if DiskSpace('{{app}}') < 2147483648 then // 2GB in bytes
  begin
    MsgBox('磁盘空间不足，至少需要2GB可用空间。', mbError, MB_OK);
    Result := False;
  end;
end;

function InitializeUninstall(): Boolean;
begin
  Result := True;
  // 在卸载前可以添加确认对话框
  if MsgBox('确定要卸载爆款视频复刻智能体吗？', mbConfirmation, MB_YESNO) = IDNO then
    Result := False;
end;
"""
    
    def package_all(self, create_installer=True, onefile=True, windowed=False):
        """打包所有内容"""
        logger.info("开始打包完整应用程序...")
        
        print("\n" + "=" * 60)
        print("爆款视频复刻智能体 - 完整打包")
        print("=" * 60)
        
        # 步骤1: 构建可执行文件
        print("\n1. 构建可执行文件...")
        if not self.build_executable(onefile=onefile, windowed=windowed):
            print("  ✗ 构建可执行文件失败")
            return False
        print("  ✓ 可执行文件构建完成")
        
        # 步骤2: 创建安装程序
        if create_installer:
            print("\n2. 创建安装程序...")
            installer_path = self.create_installer()
            if installer_path:
                print(f"  ✓ 安装程序创建完成: {Path(installer_path).name}")
            else:
                print("  ⚠ 安装程序创建失败，继续打包")
        
        # 步骤3: 创建便携版
        print("\n3. 创建便携版...")
        portable_path = self.create_portable_version()
        if portable_path:
            print(f"  ✓ 便携版创建完成: {Path(portable_path).name}")
        
        # 步骤4: 生成打包报告
        print("\n4. 生成打包报告...")
        report = self.generate_package_report()
        print(f"  ✓ 打包报告生成完成")
        
        print("\n" + "=" * 60)
        print("打包完成!")
        print("=" * 60)
        
        # 显示结果
        self._show_package_results()
        
        return True
    
    def create_portable_version(self):
        """创建便携版"""
        logger.info("创建便携版...")
        
        version = self._get_version()
        portable_name = f"VideoReplicationAgent_Portable_v{version}"
        portable_dir = self.dist_dir / portable_name
        
        try:
            # 复制文件
            if (self.dist_dir / "VideoReplicationAgent.exe").exists():
                # 单文件版本
                shutil.copy2(
                    self.dist_dir / "VideoReplicationAgent.exe",
                    portable_dir / "VideoReplicationAgent.exe"
                )
            elif (self.dist_dir / "VideoReplicationAgent").exists():
                # 目录版本
                shutil.copytree(
                    self.dist_dir / "VideoReplicationAgent",
                    portable_dir,
                    dirs_exist_ok=True
                )
            
            # 复制必要文件
            files_to_copy = [
                "README.md", "USER_GUIDE.md", "LAUNCH_GUIDE.md",
                "start.bat", "start.sh", "VERSION.json"
            ]
            
            for file_name in files_to_copy:
                src = self.dist_dir / file_name
                if src.exists():
                    shutil.copy2(src, portable_dir / file_name)
            
            # 创建便携版说明
            readme_content = f"""# 爆款视频复刻智能体 - 便携版

版本: {version}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 使用说明

### Windows用户
1. 双击运行 `start.bat`
2. 或直接运行 `VideoReplicationAgent.exe`

### Linux/macOS用户
1. 打开终端
2. 运行: `chmod +x start.sh`
3. 运行: `./start.sh`

## 功能特点

- 无需安装，解压即用
- 包含所有必要组件
- 支持离线使用（部分AI功能需要网络）
- 自动创建必要目录

## 注意事项

1. 首次运行可能会较慢（需要初始化）
2. 确保有足够的磁盘空间（至少2GB）
3. 建议在性能较好的计算机上运行

## 获取帮助

- 查看 `USER_GUIDE.md` 获取详细使用指南
- 查看 `LAUNCH_GUIDE.md` 获取启动指南
- 访问 https://openclaw.ai 获取在线帮助

---
祝您使用愉快！ 🎬✨
"""
            
            readme_file = portable_dir / "README_PORTABLE.md"
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            # 创建ZIP包
            import zipfile
            zip_path = self.dist_dir / f"{portable_name}.zip"
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in portable_dir.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(portable_dir)
                        zipf.write(file_path, arcname)
            
            # 清理临时目录
            shutil.rmtree(portable_dir)
            
            size_mb = zip_path.stat().st_size / (1024 * 1024)
            logger.info(f"便携版创建完成: {zip_path} ({size_mb:.1f} MB)")
            
            return str(zip_path)
            
        except Exception as e:
            logger.error(f"创建便携版失败: {e}")
            return None
    
    def generate_package_report(self):
        """生成打包报告"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "version": self._get_version(),
            "platform": sys.platform,
            "python_version": sys.version,
            "build_type": "executable",
            "files": [],
            "sizes": {},
            "status": "success"
        }
        
        # 收集文件信息
        if self.dist_dir.exists():
            total_size = 0
            file_count = 0
            
            for file_path in self.dist_dir.rglob("*"):
                if file_path.is_file():
                    file_info = {
                        "path": str(file_path.relative_to(self.dist_dir)),
                        "size_bytes": file_path.stat().st_size,
                        "size_mb": file_path.stat().st_size / (1024 * 1024)
                    }
                    report["files"].append(file_info)
                    
                    total_size += file_path.stat().st_size
                    file_count += 1
            
            report["sizes"] = {
                "total_files": file_count,
                "total_size_bytes": total_size,
                "total_size_mb": total_size / (1024 * 1024),
                "total_size_gb": total_size / (1024 * 1024 * 1024)
            }
        
        # 保存报告
        report_file = self.dist_dir / "PACKAGE_REPORT.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"打包报告保存到: {report_file}")
        return report
    
    def _show_package_results(self):
        """显示打包结果"""
        dist_dir = self.dist_dir
        
        if not dist_dir.exists():
            print("错误: 打包目录不存在")
            return
        
        print("\n📦 打包结果:")
        print("-" * 40)
        
        # 列出所有生成的文件
        for item in dist_dir.iterdir():
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"  📄 {item.name} ({size_mb:.1f} MB)")
            elif item.is_dir():
                dir_size = sum(f.stat().st_size for f in item.rglob('*') if f.is_file())
                size_mb = dir_size / (1024 * 1024)
                print(f"  📁 {item.name}/ ({size_mb:.1f} MB)")
        
        print("\n🚀 下一步:")
        print("  1. 测试可执行文件: 运行 dist/VideoReplicationAgent.exe --help")
        print("  2. 分发应用程序: 使用生成的安装程序或便携版")
        print("  3. 查看文档: 阅读 LAUNCH_GUIDE.md 获取详细指南")
        
        print("\n💡 提示:")
        print("  • 单文件版本适合快速分发")
        print("  • 目录版本便于调试和更新")
        print("  • 安装程序提供最佳用户体验")
        print("  • 便携版适合临时使用或演示")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="爆款视频复刻智能体 - 打包工具")
    parser.add_argument("--onefile", action="store_true", default=True,
                       help="打包为单文件可执行程序")
    parser.add_argument("--windowed", action="store_true",
                       help="创建无控制台窗口的程序")
    parser.add_argument("--debug", action="store_true",
                       help="包含调试信息")
    parser.add_argument("--installer", action="store_true",
                       help="创建安装程序")
    parser.add_argument("--portable", action="store_true",
                       help="创建便携版")
    parser.add_argument("--all", action="store_true",
                       help="执行完整打包（可执行文件+安装程序+便携版）")
    parser.add_argument("--clean", action="store_true",
                       help="清理构建目录")
    
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
        
        if args.all:
            # 完整打包
            success = packager.package_all(
                create_installer=True,
                onefile=args.onefile,
                windowed=args.windowed
            )
        else:
            # 选择性打包
            if args.onefile or args.windowed or args.debug:
                success = packager.build_executable(
                    onefile=args.onefile,
                    windowed=args.windowed,
                    debug=args.debug
                )
            
            if args.installer:
                installer_path = packager.create_installer()
                if installer_path:
                    print(f"安装程序创建完成: {installer_path}")
            
            if args.portable:
                portable_path = packager.create_portable_version()
                if portable_path:
                    print(f"便携版创建完成: {portable_path}")
        
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