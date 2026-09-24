# own.py


from openai import OpenAI
from config import config,get_conn                      

def init_db_own():
    conn = get_conn()
    cursor = conn.cursor()  
    cursor.execute("CREATE EXTENSION IF NOT EXISTS vector" )
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS own_articles (
            id SERIAL PRIMARY KEY,
            title TEXT,
            content TEXT,
            platform TEXT,
            publish_date DATE,
            views INTEGER,
            likes INTEGER,
            collects INTEGER,
            comments INTEGER,
            shares INTEGER,
            followers_gained INTEGER,
            embedding vector(1024),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()




# 95%以上的业务表都会有一个自增id，这是最稳妥、最通用的设计。




embedding_client = OpenAI(
    api_key=config.EMBEDDING_API_KEY,
    base_url=config.EMBEDDING_BASE_URL,
)

#转
def get_embedding(text):
    response = embedding_client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding
#存
def save_article(title,content,platform,publish_date,views,likes,collects,comments,shares,followers_gained):
    embedding = get_embedding(f"{title}\n{content}")
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO own_articles
        (title, content, platform, publish_date, views, likes, collects, comments, shares, followers_gained, embedding)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
       """, (title, content, platform, publish_date,
          views, likes, collects, comments, shares, followers_gained, embedding))
    conn.commit()
    conn.close()
#找
def search_viral(query, limit=5):
    query_embedding = get_embedding(query)
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT title, content FROM own_articles
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (query_embedding, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"title": r[0], "content": r[1]} for r in rows]    

#算
def get_stats_summary(platform=None):
    conn = get_conn()
    cursor = conn.cursor()

    sql = """
        SELECT
            title,
            platform,
            views,
            likes,
            collects,
            comments,
            ROUND((likes + collects + comments)::numeric / NULLIF(views, 0) * 100, 2) AS 互动率,
            ROUND(collects::numeric / NULLIF(views, 0) * 100, 2) AS 收藏率
        FROM own_articles
    """
    if platform:
        sql += " WHERE platform = %s ORDER BY 互动率 DESC"
        cursor.execute(sql, (platform,))
    else:
        sql += " ORDER BY 互动率 DESC"
        cursor.execute(sql)

    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "title": r[0],
            "platform": r[1],
            "views": r[2],
            "likes": r[3],
            "collects": r[4],
            "comments": r[5],
            "互动率": float(r[6]) if r[6] else 0,
            "收藏率": float(r[7]) if r[7] else 0,
        })
    return result