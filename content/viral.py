# viral.py

from config import get_conn
from content.own import get_embedding

from content.own import get_embedding
from content.redfox import search_xhs_notes



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



def save_viral_note(note: dict):
    """把一条红狐笔记存入 viral_articles"""
    title = note.get("workTitle", "")
    content = note.get("workDesc", "")

    embedding = get_embedding(f"{title}\n{content}")

    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO viral_articles
        (title, content, author, note_url, likes, collects, comments, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        title,
        content,
        note.get("accountNickname"),
        note.get("workUrl"),
        note.get("workLikedCount"),
        note.get("workCollectedCount"),
        note.get("workCommentsCount"),
        embedding,
    ))
    conn.commit()
    conn.close()


def fetch_and_save(keyword: str, limit: int = 10):
    """搜一批红狐笔记，存进数据库"""
    notes = search_xhs_notes(keyword)
    for note in notes:
        try:
            save_viral_note(note)
            print(f"✅ {note.get('workTitle')}")
        except Exception as e:
            print(f"❌ 失败: {e}")

            

def search_viral(query: str, limit: int = 5):
    """先按向量粗筛 20 条，再按点赞排序取前 N 条"""
    query_embedding = get_embedding(query)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, content, author, likes
        FROM viral_articles
        ORDER BY embedding <=> %s::vector
        LIMIT 20
    """, (query_embedding,))
    rows = cursor.fetchall()
    conn.close()

    results = [
        {"title": r[0], "content": r[1], "author": r[2], "likes": r[3]}
        for r in rows
    ]
    results.sort(key=lambda x: x["likes"] or 0, reverse=True)
    return results[:limit]