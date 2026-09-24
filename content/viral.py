# viral.py

from config import get_conn
from content.own import get_embedding


def init_db_viral():
    """建爆文表"""
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viral_articles (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            author TEXT,
            author_followers INTEGER,
            platform TEXT DEFAULT '小红书',
            note_url TEXT,
            likes INTEGER,
            collects INTEGER,
            comments INTEGER,
            embedding vector(1024),
            collected_date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()