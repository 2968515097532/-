"""
项目启动脚本 - 整合所有功能
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional

from loguru import logger


def setup_logging(level: str = "INFO"):
    """设置日志"""
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=level
    )


def check_environment() -> bool:
    """检查环境"""
    logger.info("检查运行环境...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
        logger.error(f"需要Python 3.8或更高版本，当前: {python_version.major}.{python_version.minor}")
        return False
    
    logger.info(f"Python版本: {python_version.major}.{python_version.minor}.{python_version.micro} ✓")
    
    # 检查必要目录
    required_dirs = ["data", "models", "logs", "temp"]
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            logger.warning(f"目录不存在，将创建: {dir_name}")
            dir_path.mkdir(parents=True, exist_ok=True)
    
    return True


def run_mode(mode: str, args: List[str]) -> bool:
    """运行指定模式"""
    logger.info(f"启动模式: {mode}")
    
    try:
        if mode == "gui":
            from src.ui.main_window import MainWindow
            from PyQt6.QtWidgets import QApplication
            
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            return app.exec()
            
        elif mode == "cli":
            from run import main as run_main
            return run_main(["cli"] + args)
            
        elif mode == "api":
            from api.server import app
            import uvicorn
            
            port = 8000
            for i, arg in enumerate(args):
                if arg == "--port" and i + 1 < len(args):
                    port = int(args[i + 1])
            
            uvicorn.run(app, host="0.0.0.0", port=port)
            return True
            
        elif mode == "admin":
            from web_admin.app import app as admin_app
            import uvicorn
            
            port = 8080
            for i, arg in enumerate(args):
                if arg == "--port" and i + 1 < len(args):
                    port = int(args[i + 1])
            
            uvicorn.run(admin_app, host="0.0.0.0", port=port)
            return True
            
        elif mode == "service":
            # 启动API和管理面板
            import threading
            import time
            
            def run_api():
                from api.server import app as api_app
                import uvicorn
                uvicorn.run(api_app, host="0.0.0.0", port=8000)
            
            def run_admin():
                from web_admin.app import app as admin_app
                import uvicorn
                uvicorn.run(admin_app, host="0.0.0.0", port=8080)
            
            api_thread = threading.Thread(target=run_api, daemon=True)
            admin_thread = threading.Thread(target=run_admin, daemon=True)
            
            api_thread.start()
            admin_thread.start()
            
            logger.info("服务已启动:")
            logger.info("  API服务: http://localhost:8000")
            logger.info("  管理面板: http://localhost:8080/admin")
            logger.info("  按 Ctrl+C 停止服务")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("正在停止服务...")
                return True
            
        elif mode == "test":
            from scripts.test_system import SystemTester
            tester = SystemTester()
            return tester.run_all_tests()
            
        elif mode == "optimize":
            from scripts.optimize_models import main as optimize_main
            return optimize_main()
            
        elif mode == "monitor":
            from scripts.monitor_system import SystemMonitor
            monitor = SystemMonitor()
            monitor.start_monitoring()
            
            logger.info("系统监控已启动，按 Ctrl+C 停止")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                monitor.stop_monitoring()
                return True
            
        elif mode == "init":
            from init_project import main as init_main
            return init_main()
            
        elif mode == "deploy":
            from deploy import main as deploy_main
            return deploy_main()
            
        else:
            logger.error(f"未知模式: {mode}")
            return False
            
    except ImportError as e:
        logger.error(f"导入模块失败: {e}")
        logger.info("请先运行: python init_project.py")
        return False
    except Exception as e:
        logger.error(f"运行模式 {mode} 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_banner():
    """打印横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      🎬 爆款视频复刻智能体 - 视频创作革命 🎬             ║
    ║                                                          ║
    ║   从视频链接到复刻完成，全自动智能处理                   ║
    ║   支持人脸替换、文案重写、视频编辑一体化                 ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    
    版本: 1.0.0 | 开源免费 | 技术支持: https://github.com/openclaw
    
    """
    print(banner)


def print_help():
    """打印帮助信息"""
    help_text = """
使用方法:
  python launch.py [模式] [选项]

可用模式:
  gui         启动图形界面 (推荐)
  cli         命令行模式
  api         启动API服务
  admin       启动管理面板
  service     启动完整服务 (API + 管理面板)
  test        运行系统测试
  optimize    优化模型性能
  monitor     系统监控
  init        项目初始化
  deploy      部署项目

示例:
  python launch.py gui                    # 启动图形界面
  python launch.py cli --url "..." --image "..."  # 命令行处理
  python launch.py api --port 8000       # 启动API服务
  python launch.py service               # 启动完整服务
  python launch.py test                  # 运行系统测试

快速开始:
  1. python launch.py init               # 初始化项目
  2. python launch.py test               # 运行测试
  3. python launch.py gui                # 启动图形界面

更多帮助:
  查看 README.md 或运行: python launch.py --help
    """
    print(help_text)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="爆款视频复刻智能体启动器", add_help=False)
    parser.add_argument("mode", nargs="?", help="运行模式")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="模式参数")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    parser.add_argument("--help", "-h", action="store_true", help="显示帮助")
    
    # 解析参数
    if len(sys.argv) == 1:
        print_banner()
        print_help()
        return
    
    args = parser.parse_args()
    
    # 设置日志级别
    log_level = "DEBUG" if args.debug else "INFO"
    setup_logging(log_level)
    
    # 显示帮助
    if args.help or args.mode is None:
        print_banner()
        print_help()
        return
    
    # 检查环境
    if not check_environment():
        logger.error("环境检查失败，请先运行: python init_project.py")
        return
    
    # 打印横幅
    print_banner()
    
    # 运行指定模式
    success = run_mode(args.mode, args.args)
    
    if success:
        logger.info(f"模式 {args.mode} 执行完成")
    else:
        logger.error(f"模式 {args.mode} 执行失败")


if __name__ == "__main__":
    main()