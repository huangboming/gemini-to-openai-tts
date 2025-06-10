import logging
import sys

from app.core.config import settings


def setup_logging(log_level: str | None = None) -> None:
    """
    设置应用程序的日志配置。

    Args:
        log_level: 日志级别，如果未提供则使用配置文件中的设置
    """
    level = log_level or settings.LOG_LEVEL

    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 配置根日志器
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format=log_format,
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,  # 强制重新配置，覆盖任何现有配置
    )

    # 为第三方库设置更高的日志级别，减少噪音
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("google").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    获取指定名称的日志器。

    Args:
        name: 日志器名称，通常使用 __name__

    Returns:
        配置好的日志器实例
    """
    return logging.getLogger(name)


# 应用启动时设置日志
setup_logging()
