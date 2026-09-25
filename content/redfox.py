# redfox.py

import os
from redfox import RedFoxClient

client = RedFoxClient(api_key=os.getenv("REDFOX_API_KEY"))


def search_xhs_notes(keyword: str, sort_type: str = "4"):
    result = client.xiaohongshu.search_articles(
        keyword=keyword,
        sort_type=sort_type,
    )
    return result.get("list", [])