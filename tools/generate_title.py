#generate_title.py 生成标题

def generate_title(topic: str, count: int = 5, style: str = "正式") -> str:
    return f"""
请根据以下主题，生成{count}个淘宝/小红书风格的电商标题。

主题：{topic}
风格：{style}

要求：
1. 每个标题独立成行，不要序号
2. 标题要有吸引力，能让人想点进去
3. 可以带 emoji（小红书风格时）
4. 突出卖点：材质、版型、场景、人群
5. 不要写成研究报告或论文标题
6. 只输出标题，不要加任何解释
"""