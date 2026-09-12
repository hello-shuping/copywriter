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



def load_history(user_id: str, limit: int = 20, system_prompt: str = ""):
    """
    加载用户最近 limit 条历史记录
    
    参数：
        user_id: 用户ID
        limit: 加载条数（默认20）
        system_prompt: 系统提示词，会放在消息列表最前面（由外部传入）
    
    返回：
        messages: 可直接用于大模型调用的消息列表
    """
    conn = psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_DATABASE,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_input, ai_reply FROM conversations WHERE user_id = %s ORDER BY created_at DESC LIMIT %s",
        (user_id, limit)
    )
    rows = cursor.fetchall()
    rows.reverse()  # 从旧到新排序

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    for user_msg, ai_msg in rows:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})
    conn.close()
    return messages 

