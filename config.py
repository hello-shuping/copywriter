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
    AUTH_KEY = os.getenv("AUTH_KEY", "").strip() #API_KEY鉴权
    #LLM API配置
    MODEL = os.getenv("MODEL")
    API_KEY = os.getenv("API_KEY","")
    BASE_URL = os.getenv("BASE_URL")
    #LLM 默认参数
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT","你是一个有用的助手")
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE","0.7"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH","5"))
    MAX_INPUT_LENGTH = int(os.getenv("MAX_INPUT_LENGTH", "2000"))

    #应用元数据
    APP_TITLE = os.getenv("APP_TITLE","Copywriter Agent")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION","AI文案助手")
    APP_VERSION = os.getenv("APP_VERSION","1.0.0")
    #服务器配置
    API_HOST = os.getenv("API_HOST")
    API_PORT = int(os.getenv("API_PORT"))
    RELOAD = os.getenv("RELOAD", "true").lower() in ("true", "1", "yes")  # 注意：.env 里写 true / True / 1 都会被转成布尔值


    # 数据库
    DB_HOST = os.getenv("DB_HOST","localhost")
    DB_PORT = int(os.getenv("DB_PORT","5432"))
    DB_DATABASE = os.getenv("DB_DATABASE","postgres")
    DB_USER = os.getenv("DB_USER","postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD","")
    EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
    EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "")
    # config.py 末尾加

    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_DATABASE", "postgres"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", ""),
    }

    
config = Config()

def get_conn():
    import psycopg2
    return psycopg2.connect(**config.DB_CONFIG)


