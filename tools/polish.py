#polish.py 润色

def polish(text: str, style: str = "正式") -> str:
    style_map = {
        "正式": "使用严谨、专业的商务用语，措辞书面化",
        "轻松": "使用轻松、活泼的口语表达，像朋友聊天",
        "简洁": "用最少的字表达最清晰的意思，句子短",
        "小红书": "小红书风格，带emoji，语气亲切，像推荐好物"    
    }
    style_desc = style_map.get(style, style_map["正式"])
    return f"""

请将以下文案润色成「{style}」风格。
风格要求：{style_desc}
原文：
{text}
只输出润色后的结果，不要加任何解释。

"""