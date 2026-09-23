def generate_title(topic: str, count: int = 5, style: str = "淘宝") -> str:
    style_map = {
        "淘宝": "30字以内，空格分隔无标点，含至少3个搜索关键词，直白硬核不夸张",
        "小红书": "25字以内，含1个Emoji，提到特定人群（打工人/学生党/微胖女孩），口语化像闺蜜分享",
    }

    current_rules = style_map.get(style, style_map["淘宝"])

    return f"""生成 {count} 个「{style}」风格标题，主题：{topic}。

规则：{current_rules}

只输出标题，每行一个，不要解释。"""