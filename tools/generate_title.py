#generate_title.py 生成标题

def generate_title(topic:str,count:int=5,style:str="正式") -> str:
    style_map = {
        "正式": "措辞严谨，适合职场或专业场景",
        "吸引眼球": "有冲击力，让人想点进去看",
        "故事感": "像讲故事一样，有画面感",
        "干货型": "强调价值，让人感觉学到东西"
    }
    style_desc = style_map.get(style,style_map["正式"])    #.get(参数,默认值:找不到时返回)
    return f"""

请根据以下主题，生成{count}个「{style}」风格的标题。
主题：{topic}
风格要求：{style_desc}
要求：
1. 每个标题独立成行
2. 不要加序号
3. 只输出标题，不要加任何解释

"""