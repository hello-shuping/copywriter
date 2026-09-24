#analyze_stats.py

from viral.gss import get_stats_summary


def analyze_stats(platform: str = "小红书") -> str:
    """拉数据，拼成 prompt，让大模型分析"""
    data = get_stats_summary(platform)

    if not data:
        return "暂无数据"

    lines = []
    for d in data:
        lines.append(
            f"- {d['title']} | 阅读{d['views']} | 点赞{d['likes']} "
            f"| 收藏{d['collects']} | 互动率{d['互动率']}% | 收藏率{d['收藏率']}%"
        )

    data_text = "\n".join(lines)

    return f"""以下是{platform}最近的文案数据，请分析：

{data_text}

请回答：
1. 哪几篇表现最好？为什么？
2. 标题有什么共性规律？
3. 下一篇该怎么写？
"""