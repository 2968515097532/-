#!/usr/bin/env python3
"""
爆款视频复刻智能体 - 主程序入口
"""

import argparse
import sys
import os
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from config import LOG_CONFIG, UI_CONFIG

# 配置日志
logger.remove()
logger.add(
    sys.stderr,
    level=LOG_CONFIG["level"],
    format=LOG_CONFIG["format"]
)
logger.add(
    "logs/app.log",
    rotation=LOG_CONFIG["rotation"],
    retention=LOG_CONFIG["retention"],
    level="DEBUG"
)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="爆款视频复刻智能体")
    parser.add_argument("--url", type=str, help="目标视频链接")
    parser.add_argument("--image", type=str, help="用户人物图片路径")
    parser.add_argument("--output", type=str, default="output.mp4", help="输出视频路径")
    parser.add_argument("--gui", action="store_true", help="启动GUI界面")
    parser.add_argument("--api", action="store_true", help="启动API服务")
    parser.add_argument("--port", type=int, default=8000, help="API服务端口")
    parser.add_argument("--debug", action="store_true", help="调试模式")
    
    args = parser.parse_args()
    
    if args.debug:
        logger.level("DEBUG")
        logger.debug("调试模式已启用")
    
    try:
        if args.gui:
            # 启动GUI界面
            from ui.main_window import MainWindow
            from PyQt6.QtWidgets import QApplication
            
            app = QApplication(sys.argv)
            window = MainWindow()
            window.show()
            sys.exit(app.exec())
            
        elif args.api:
            # 启动API服务
            from api.server import app
            import uvicorn
            
            logger.info(f"启动API服务，端口: {args.port}")
            uvicorn.run(app, host="0.0.0.0", port=args.port)
            
        elif args.url and args.image:
            # 命令行模式
            from src.video_replicator import VideoReplicator
            
            logger.info(f"开始处理视频: {args.url}")
            logger.info(f"使用图片: {args.image}")
            logger.info(f"输出到: {args.output}")
            
            replicator = VideoReplicator()
            result = replicator.replicate(
                video_url=args.url,
                user_image=args.image,
                output_path=args.output
            )
            
            if result["success"]:
                logger.success(f"视频处理完成: {result['output_path']}")
                logger.info(f"处理耗时: {result['processing_time']:.2f}秒")
            else:
                logger.error(f"处理失败: {result['error']}")
                sys.exit(1)
                
        else:
            parser.print_help()
            print("\n示例:")
            print("  python main.py --url https://www.douyin.com/video/123 --image user.jpg --output result.mp4")
            print("  python main.py --gui")
            print("  python main.py --api --port 8000")
            
    except KeyboardInterrupt:
        logger.info("用户中断操作")
        sys.exit(0)
    except Exception as e:
        logger.exception(f"程序运行出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()