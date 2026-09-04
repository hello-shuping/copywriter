import psycopg2
from datetime import datetime
from config import config

from logger import logger                              #日志

def init_db():
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_DATABASE,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id SERIAL PRIMARY KEY,             
            user_id TEXT,
            user_input TEXT,
            ai_reply TEXT,
            created_at TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()

# 95%以上的业务表都会有一个自增id，这是最稳妥、最通用的设计。


def save_to_db(user_id, user_input, ai_reply):
    try:                                              #日志

        conn = psycopg2.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            database=config.DB_DATABASE,
            user=config.DB_USER,
            password=config.DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_id, user_input, ai_reply, created_at) VALUES (%s, %s, %s, %s)",
            (user_id, user_input, ai_reply, datetime.now())
        )
        conn.commit()
        conn.close()

        logger.info(f"✅ 用户 {user_id} 对话已保存")    #日志
    except Exception as e:                             #日志
        logger.error(f"❌ 数据库写入失败: {e}")         #日志