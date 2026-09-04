#config.py
#使用指南：支持2种导入方式
#1、from config import Config   (导入类，自己实例化)
#       cfg=Config()
#       api_key=cfg.DEEPSEEK_API_KEY
#2、from config import config
#   api_key=cfg.DEEPSEEK_API_KEY

import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    # API配置
    MODEL = os.getenv("MODEL")
    API_KEY = os.getenv("API_KEY")
    BASE_URL = os.getenv("BASE_URL")
    

    # Agent默认参数
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT","你是一个有用的助手")
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE","0.7"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH","20"))

    # 服务器配置
    API_HOST = os.getenv("API_HOST","0.0.0.0")
    API_PORT = int(os.getenv("API_PORT","8000"))
    RELOAD = os.getenv("RELOAD","True")

    # FastAPI应用元数据
    APP_TITLE = os.getenv("APP_TITLE","Agent API")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION","通用Agent服务")
    APP_VERSION = os.getenv("APP_VERSION","1.0.0")

    # 数据库
    DB_HOST = os.getenv("DB_HOST","localhost")
    DB_PORT = int(os.getenv("DB_PORT","5432"))
    DB_DATABASE = os.getenv("DB_DATABASE","postgres")
    DB_USER = os.getenv("DB_USER","postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD","psql911105")
    
config = Config()



