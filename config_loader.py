            if format.lower() == "json":
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            elif format.lower() in ["yaml", "yml"]:
                with open(filepath, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            else:
                logger.warning(f"不支持的配置文件格式: {format}")
                return
            
            logger.info(f"配置保存到文件: {filepath}")
            
        except Exception as e:
            logger.error(f"保存配置文件失败 {filepath}: {e}")
    
    def validate(self) -> bool:
        """验证配置"""
        errors = []
        
        # 检查必要目录
        required_dirs = [
            self.storage.data_dir,
            self.storage.models_dir,
            self.storage.logs_dir,
            self.storage.temp_dir
        ]
        
        for dir_path in required_dirs:
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                errors.append(f"创建目录失败 {dir_path}: {e}")
        
        # 检查模型文件
        if not Path(self.models.face_detection["model_path"]).exists():
            errors.append(f"人脸检测模型不存在: {self.models.face_detection['model_path']}")
        
        if not Path(self.models.face_swap["model_path"]).exists():
            errors.append(f"人脸替换模型不存在: {self.models.face_swap['model_path']}")
        
        # 检查端口范围
        if not (1 <= self.api_port <= 65535):
            errors.append(f"API端口超出范围: {self.api_port}")
        
        if not (1 <= self.admin_port <= 65535):
            errors.append(f"管理面板端口超出范围: {self.admin_port}")
        
        # 检查存储空间
        if self.storage.max_storage_size <= 0:
            errors.append(f"最大存储空间必须大于0: {self.storage.max_storage_size}")
        
        # 输出错误
        if errors:
            for error in errors:
                logger.error(f"配置验证失败: {error}")
            return False
        
        logger.info("配置验证通过")
        return True
    
    def get_source(self, config_path: str) -> ConfigSource:
        """获取配置来源"""
        return self._sources.get(config_path, ConfigSource.DEFAULT)
    
    def summary(self) -> Dict[str, Any]:
        """获取配置摘要"""
        return {
            "app": {
                "name": self.app_name,
                "version": self.app_version,
                "debug": self.debug,
                "test_mode": self.test_mode
            },
            "server": {
                "api_host": self.api_host,
                "api_port": self.api_port,
                "admin_port": self.admin_port
            },
            "paths": {
                "data_dir": self.storage.data_dir,
                "models_dir": self.storage.models_dir,
                "logs_dir": self.storage.logs_dir,
                "temp_dir": self.storage.temp_dir
            },
            "models": {
                "face_detection": self.models.face_detection["model_path"],
                "face_swap": self.models.face_swap["model_path"],
                "text_model": self.models.text_rewrite["model_name"]
            },
            "performance": {
                "max_workers": self.max_workers,
                "memory_limit": self.memory_limit
            },
            "security": {
                "enable_auth": self.security.enable_auth,
                "max_file_size": self.security.max_file_size
            }
        }
    
    def print_summary(self):
        """打印配置摘要"""
        summary = self.summary()
        
        print("=" * 60)
        print("爆款视频复刻智能体 - 配置摘要")
        print("=" * 60)
        
        for category, configs in summary.items():
            print(f"\n{category.upper()}:")
            for key, value in configs.items():
                print(f"  {key}: {value}")
        
        print("\n" + "=" * 60)


# 全局配置实例
_config_instance: Optional[AppConfig] = None


def init_config(
    config_file: Optional[str] = None,
    env_file: Optional[str] = None,
    base_dir: Optional[str] = None
) -> AppConfig:
    """初始化配置"""
    global _config_instance
    
    if _config_instance is not None:
        return _config_instance
    
    # 确定基础目录
    if base_dir is None:
        base_dir = Path(__file__).parent
    
    # 创建默认配置
    config = AppConfig(base_dir=str(base_dir))
    
    # 加载环境变量
    if env_file:
        env_path = Path(env_file)
        if env_path.exists():
            dotenv.load_dotenv(env_path)
        else:
            # 尝试默认的.env文件
            default_env = base_dir / ".env"
            if default_env.exists():
                dotenv.load_dotenv(default_env)
    
    # 从环境变量更新
    config.update_from_env()
    
    # 加载配置文件
    if config_file:
        config.load_from_file(config_file)
    else:
        # 尝试默认配置文件
        default_files = [
            base_dir / "config.json",
            base_dir / "config.yaml",
            base_dir / "config.yml"
        ]
        
        for file in default_files:
            if file.exists():
                config.load_from_file(str(file))
                break
    
    # 验证配置
    if not config.validate():
        logger.warning("配置验证失败，某些功能可能无法正常工作")
    
    _config_instance = config
    return config


def get_config() -> AppConfig:
    """获取配置实例"""
    global _config_instance
    
    if _config_instance is None:
        _config_instance = init_config()
    
    return _config_instance


def reload_config(config_file: Optional[str] = None) -> AppConfig:
    """重新加载配置"""
    global _config_instance
    _config_instance = None
    return init_config(config_file)


# 配置工具函数
def setup_environment():
    """设置环境"""
    config = get_config()
    
    # 设置日志
    import sys
    from loguru import logger
    
    logger.remove()
    logger.add(
        sys.stderr,
        format=config.logs.format,
        level=config.logs.level
    )
    
    # 添加文件日志
    log_file = Path(config.storage.logs_dir) / "app_{time}.log"
    logger.add(
        str(log_file),
        rotation=config.logs.rotation,
        retention=config.logs.retention,
        compression=config.logs.compression,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG" if config.debug else config.logs.level
    )
    
    # 设置时区
    import os
    os.environ['TZ'] = 'Asia/Shanghai'
    
    # 创建必要目录
    for dir_path in [
        config.storage.data_dir,
        config.storage.models_dir,
        config.storage.logs_dir,
        config.storage.temp_dir
    ]:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    logger.info("环境设置完成")
    return config


def check_dependencies():
    """检查依赖"""
    import importlib
    import pkgutil
    
    required_packages = [
        "torch",
        "torchvision",
        "opencv_python",
        "moviepy",
        "yt_dlp",
        "insightface",
        "onnxruntime",
        "transformers",
        "PyQt6",
        "fastapi",
        "uvicorn",
        "loguru",
        "psutil"
    ]
    
    missing = []
    for package in required_packages:
        try:
            importlib.import_module(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.warning(f"缺少依赖包: {', '.join(missing)}")
        logger.info(f"请运行: pip install {' '.join(missing)}")
        return False
    
    logger.info("所有依赖包已安装")
    return True


def setup_models():
    """设置模型"""
    config = get_config()
    
    # 检查模型文件
    models_to_check = [
        ("人脸检测", config.models.face_detection["model_path"]),
        ("人脸替换", config.models.face_swap["model_path"])
    ]
    
    missing_models = []
    for model_name, model_path in models_to_check:
        if not Path(model_path).exists():
            missing_models.append((model_name, model_path))
    
    if missing_models:
        logger.warning("缺少模型文件:")
        for model_name, model_path in missing_models:
            logger.warning(f"  {model_name}: {model_path}")
        
        # 尝试自动下载
        try:
            from download_models import download_all_models
            logger.info("尝试自动下载模型...")
            if download_all_models():
                logger.info("模型下载完成")
            else:
                logger.error("模型下载失败，请手动下载")
                return False
        except ImportError:
            logger.error("无法自动下载模型，请手动下载")
            return False
    
    logger.info("模型设置完成")
    return True


if __name__ == "__main__":
    # 测试配置加载
    config = init_config()
    config.print_summary()
    
    # 验证配置
    if config.validate():
        print("\n配置验证: ✓ 通过")
    else:
        print("\n配置验证: ✗ 失败")