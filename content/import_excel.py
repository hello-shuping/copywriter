
import time
import pandas as pd
from content.own import save_article


def import_from_excel(path):
    # ===== 新增：先清空表，再导入 =====
    from config import get_conn
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM articles")
    conn.commit()
    conn.close()
    # ===== 新增结束 =====
    df = pd.read_excel(path)

def import_from_excel(path):
    df = pd.read_excel(path)
    print(f"共 {len(df)} 行")

    success = 0
    for i, row in df.iterrows():
        try:
            save_article(
                title=str(row["title"]).strip(),
                content=str(row["content"]).replace("|||", "\n\n"),
                platform=str(row.get("platform", "小红书")),
                publish_date=row.get("publish_date"),
                views=int(row.get("views", 0) or 0),
                likes=int(row.get("likes", 0) or 0),
                collects=int(row.get("collects", 0) or 0),
                comments=int(row.get("comments", 0) or 0),
                shares=int(row.get("shares", 0) or 0),
                followers_gained=int(row.get("followers_gained", 0) or 0),
            )
            success += 1
            print(f"✅ {i+1}/{len(df)}：{row['title']}")
            time.sleep(0.5)   # 防止 embedding API 限流
        except Exception as e:
            print(f"❌ 第 {i+2} 行失败：{e}")

    print(f"\n导入完成：成功 {success}/{len(df)}")


if __name__ == "__main__":
    import_from_excel("articles.xlsx")