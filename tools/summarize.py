#summarize.py 总结

def summarize(text: str, length: str = "简短") -> str:
    length_map = {
        "简短": "3-5句话，核心观点",
        "详细": "一段完整的摘要，包含主要论点和结论"
    }
    length_desc = length_map.get(length, length_map["简短"])
    return f"""

请用「{length}」的方式总结以下内容。
{length_desc}
原文：
{text}
只输出总结结果，不要加任何解释。

"""
