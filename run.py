"""
项目运行脚本
统一管理所有运行模式
"""

import argparse
import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from loguru import logger
from monitor import init_monitoring, shutdown_monitoring


def setup_logging():
    """设置日志"""
    # 移除默认配置
    logger.remove()
    
    # 控制台输出
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    # 文件输出
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "app_{time}.log",
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG"
    )


def run_cli_mode(args):
    """运行命令行模式"""
    from main import main as cli_main
    
    # 构建命令行参数
    sys.argv = ["main.py"]
    
    if args.url:
        sys.argv.extend(["--url", args.url])
    
    if args.image:
        sys.argv.extend(["--image", args.image])
    
    if args.output:
        sys.argv.extend(["--output", args.output])
    
    if args.style:
        sys.argv.extend(["--style", args.style])
    
    if args.no_face_swap:
        sys.argv.append("--no-face-swap")
    
    if args.no_subtitles:
        sys.argv.append("--no-subtitles")
    
    if args.debug:
        sys.argv.append("--debug")
    
    # 运行主程序
    cli_main()


def run_gui_mode():
    """运行GUI模式"""
    try:
        from PyQt6.QtWidgets import QApplication
        from src.ui.main_window import MainWindow
        
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
        
    except ImportError as e:
        logger.error(f"GUI模式需要PyQt6: {e}")
        print("请安装PyQt6: pip install PyQt6")
        sys.exit(1)


def run_api_mode(args):
    """运行API模式"""
    try:
        import uvicorn
        from api.server import app as api_app
        
        logger.info(f"启动API服务，端口: {args.port}")
        logger.info(f"API文档: http://localhost:{args.port}/docs")
        
        uvicorn.run(
            api_app,
            host=args.host,
            port=args.port,
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"API模式需要FastAPI: {e}")
        print("请安装FastAPI: pip install fastapi uvicorn")
        sys.exit(1)


def run_admin_mode(args):
    """运行管理面板模式"""
    try:
        import uvicorn
        from web_admin.app import app as admin_app
        
        logger.info(f"启动管理面板，端口: {args.port}")
        logger.info(f"管理面板: http://localhost:{args.port}/admin")
        logger.info(f"API文档: http://localhost:{args.port}/admin/docs")
        
        uvicorn.run(
            admin_app,
            host=args.host,
            port=args.port,
            log_level="info"
        )
        
    except ImportError as e:
        logger.error(f"管理面板需要FastAPI: {e}")
        print("请安装FastAPI: pip install fastapi uvicorn jinja2")
        sys.exit(1)


def run_batch_mode(args):
    """运行批量处理模式"""
    try:
        from src.video_replicator import VideoReplicator
        from src.video_replicator import ReplicationConfig, RewriteStyle
        
        # 读取任务文件
        import json
        with open(args.task_file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        if not isinstance(tasks, list):
            logger.error("任务文件必须是JSON数组")
            sys.exit(1)
        
        # 创建复刻器
        replicator = VideoReplicator()
        
        # 准备数据
        video_urls = []
        user_images = []
        
        for task in tasks:
            if 'video_url' not in task or 'user_image' not in task:
                logger.warning(f"任务缺少必要字段: {task}")
                continue
            
            video_urls.append(task['video_url'])
            user_images.append(task['user_image'])
        
        if not video_urls:
            logger.error("没有有效的任务")
            sys.exit(1)
        
        # 创建输出目录
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置
        config = ReplicationConfig(
            rewrite_style=RewriteStyle(args.style),
            keep_temp_files=args.keep_temp
        )
        
        # 执行批量处理
        logger.info(f"开始批量处理 {len(video_urls)} 个任务")
        
        result = replicator.batch_replicate(
            video_urls=video_urls,
            user_images=user_images,
            output_dir=str(output_dir),
            config=config
        )
        
        # 保存结果
        result_file = output_dir / "batch_result.json"
        import json
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        logger.info(f"批量处理完成，结果保存到: {result_file}")
        
        # 显示摘要
        print(f"\n{'='*60}")
        print("批量处理摘要:")
        print(f"{'='*60}")
        print(f"总计任务: {result['total']}")
        print(f"成功: {result['successful']}")
        print(f"失败: {result['failed']}")
        print(f"成功率: {result['success_rate']:.2%}")
        
        if result['failed'] > 0:
            print(f"\n失败任务:")
            for i, task_result in enumerate(result['results']):
                if not task_result['success']:
                    print(f"  任务{i+1}: {task_result.get('error', '未知错误')}")
        
    except Exception as e:
        logger.error(f"批量处理失败: {e}")
        sys.exit(1)


def run_service_mode(args):
    """运行服务模式（API + 管理面板）"""
    try:
        import uvicorn
        import threading
        import time
        
        from api.server import app as api_app
        from web_admin.app import app as admin_app
        
        # 修改管理面板的端口
        admin_port = args.admin_port
        
        # 启动API服务（在子线程中）
        def run_api():
            uvicorn.run(
                api_app,
                host=args.host,
                port=args.port,
                log_level="warning"  # 减少日志输出
            )
        
        # 启动管理面板（在子线程中）
        def run_admin():
            uvicorn.run(
                admin_app,
                host=args.host,
                port=admin_port,
                log_level="warning"
            )
        
        logger.info("启动服务模式...")
        logger.info(f"API服务: http://{args.host}:{args.port}")
        logger.info(f"管理面板: http://{args.host}:{admin_port}/admin")
        logger.info(f"API文档: http://{args.host}:{args.port}/docs")
        
        # 启动线程
        api_thread = threading.Thread(target=run_api, daemon=True)
        admin_thread = threading.Thread(target=run_admin, daemon=True)
        
        api_thread.start()
        admin_thread.start()
        
        # 等待线程启动
        time.sleep(2)
        
        logger.info("服务已启动，按Ctrl+C停止")
        
        # 保持主线程运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("正在停止服务...")
            
    except Exception as e:
        logger.error(f"服务模式启动失败: {e}")
        sys.exit(1)


def run_test_mode(args):
    """运行测试模式"""
    try:
        # 运行单元测试
        import unittest
        import tests.test_basic
        
        logger.info("运行单元测试...")
        
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # 添加测试
        suite.addTests(loader.loadTestsFromModule(tests.test_basic))
        
        # 运行测试
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            logger.info("所有测试通过!")
        else:
            logger.error("部分测试失败!")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"测试运行失败: {e}")
        sys.exit(1)


def run_demo_mode(args):
    """运行演示模式"""
    try:
        from examples.basic_usage import main as demo_main
        
        logger.info("运行演示程序...")
        demo_main()
        
    except Exception as e:
        logger.error(f"演示程序运行失败: {e}")
        sys.exit(1)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="爆款视频复刻智能体 - 统一运行脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 命令行模式
  python run.py cli --url "视频链接" --image "用户图片.jpg"
  
  # GUI模式
  python run.py gui
  
  # API模式
  python run.py api --port 8000
  
  # 管理面板
  python run.py admin --port 8080
  
  # 服务模式 (API + 管理面板)
  python run.py service
  
  # 批量处理
  python run.py batch --task-file tasks.json --output-dir results/
  
  # 测试模式
  python run.py test
  
  # 演示模式
  python run.py demo
        """
    )
    
    # 子命令
    subparsers = parser.add_subparsers(dest="mode", help="运行模式")
    
    # CLI模式
    cli_parser = subparsers.add_parser("cli", help="命令行模式")
    cli_parser.add_argument("--url", required=True, help="视频链接")
    cli_parser.add_argument("--image", required=True, help="用户图片路径")
    cli_parser.add_argument("--output", help="输出视频路径")
    cli_parser.add_argument("--style", default="casual", 
                          choices=["humorous", "formal", "casual", "persuasive"],
                          help="文案风格")
    cli_parser.add_argument("--no-face-swap", action="store_true", help="禁用人脸替换")
    cli_parser.add_argument("--no-subtitles", action="store_true", help="禁用字幕")
    cli_parser.add_argument("--debug", action="store_true", help="调试模式")
    
    # GUI模式
    gui_parser = subparsers.add_parser("gui", help="图形界面模式")
    
    # API模式
    api_parser = subparsers.add_parser("api", help="API服务模式")
    api_parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    api_parser.add_argument("--port", type=int, default=8000, help="监听端口")
    
    # 管理面板模式
    admin_parser = subparsers.add_parser("admin", help="管理面板模式")
    admin_parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    admin_parser.add_argument("--port", type=int, default=8080, help="监听端口")
    
    # 服务模式
    service_parser = subparsers.add_parser("service", help="服务模式 (API + 管理面板)")
    service_parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    service_parser.add_argument("--port", type=int, default=8000, help="API端口")
    service_parser.add_argument("--admin-port", type=int, default=8080, help="管理面板端口")
    
    # 批量处理模式
    batch_parser = subparsers.add_parser("batch", help="批量处理模式")
    batch_parser.add_argument("--task-file", required=True, help="任务JSON文件")
    batch_parser.add_argument("--output-dir", required=True, help="输出目录")
    batch_parser.add_argument("--style", default="casual",
                            choices=["humorous", "formal", "casual", "persuasive"],
                            help="文案风格")
    batch_parser.add_argument("--keep-temp", action="store_true", help="保留临时文件")
    
    # 测试模式
    test_parser = subparsers.add_parser("test", help="测试模式")
    
    # 演示模式
    demo_parser = subparsers.add_parser("demo", help="演示模式")
    
    # 解析参数
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    # 设置日志
    setup_logging()
    
    # 初始化监控
    init_monitoring()
    
    try:
        # 根据模式运行
        if args.mode == "cli":
            run_cli_mode(args)
        elif args.mode == "gui":
            run_gui_mode()
        elif args.mode == "api":
            run_api_mode(args)
        elif args.mode == "admin":
            run_admin_mode(args)
        elif args.mode == "service":
            run_service_mode(args)
        elif args.mode == "batch":
            run_batch_mode(args)
        elif args.mode == "test":
            run_test_mode(args)
        elif args.mode == "demo":
            run_demo_mode(args)
        else:
            logger.error(f"未知模式: {args.mode}")
            parser.print_help()
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("用户中断操作")
    except Exception as e:
        logger.exception(f"运行失败: {e}")
        sys.exit(1)
    finally:
        # 关闭监控
        shutdown_monitoring()


if __name__ == "__main__":
    main()