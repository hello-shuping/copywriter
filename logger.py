import logging
import sys
from datetime import datetime

def setup_logger(name: str = "app") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 控制台输出（只显示 INFO 及以上）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)

    # 文件输出（显示 DEBUG 及以上，按天切割）
    file_handler = logging.FileHandler(f"logs/app_{datetime.now().strftime('%Y%m%d')}.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)

    # 统一格式
    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# 默认 logger 实例
logger = setup_logger()