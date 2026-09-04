#agent.py
#agent.py 同步版vs异步版 
#from openai import OpenAI ------->  from openai import AsyncOpenAI
#client = OpenAI(...)     ---------->      client = AsyncOpenAI(...)
#def chat(user_input):    ---------->      async def chat(user_input):
#response = client.chat.... -----> response = await client.chat...   


from openai import AsyncOpenAI
from config import config 
from db.ccs import init_db,save_to_db

import json
from tools import TOOLS

from logger import logger        #日志



client = AsyncOpenAI(
    api_key = config.API_KEY,
    base_url=config.BASE_URL
    )

init_db()

user_histories={} #字典

async def chat(user_id,user_input):
    logger.info(f"用户 {user_id} 输入: {user_input}")         #日志
    if user_id not in user_histories:
        user_histories[user_id]=[{"role":"system","content":config.SYSTEM_PROMPT}]
    user_histories[user_id].append({"role":"user","content":user_input})



    #第1次调用大模型
    response = await client.chat.completions.create(
        model=config.MODEL,
        messages=user_histories[user_id],  #列表
        )
    ai_reply=response.choices[0].message.content
    logger.debug(f"大模型首次返回: {ai_reply}")                 #日志
    #判断是否使用工具
    if ai_reply.startswith("{") and "tool" in ai_reply:
        logger.info(f"检测到工具调用: {ai_reply}")              #日志
        data=json.loads(ai_reply)
        tool_name = data["tool"]
        tool_params = data["params"]
        tool_prompt = TOOLS[tool_name](**tool_params)
        logger.info(f"工具 {tool_name} 执行完成")               #日志    
    
    #第2次调用大模型
        response2 = await client.chat.completions.create(
        model=config.MODEL,
        messages=[{"role": "user", "content": tool_prompt}],  
        )
        ai_reply=response2.choices[0].message.content  
    else:
    # 兜底逻辑：检测关键词，自动补全工具调用
        logger.info("未检测到工具调用，尝试关键词匹配...")
        user_input_lower = user_input.lower()
    
    # 定义关键词与工具的映射
        keyword_tool_map = {
            "润色": {"tool": "polish", "params": {"text": "", "style": "正式"}},
            "改写": {"tool": "polish", "params": {"text": "", "style": "正式"}},
            "生成标题": {"tool": "generate_title", "params": {"topic": "", "count": 5, "style": "正式"}},
            "写文章": {"tool": "write_article", "params": {"topic": "", "word_count": 1200, "style": "正式"}},
            "总结": {"tool": "summarize", "params": {"text": "", "length": "简短"}},
            }
        tool_to_call = None
        for keyword, tool_info in keyword_tool_map.items():
            if keyword in user_input:
                # 提取内容（简单提取：去除关键词，取剩余部分）
                # 去除常见前缀词
                prefixes_to_remove = ["这段文案：", "这段话：", "这段文字：", "文案：", "内容：", "："]
                for prefix in prefixes_to_remove:
                    if remaining.startswith(prefix):
                        remaining = remaining[len(prefix):].strip()
                        break
                if remaining:
                    # 如果关键词在开头，剩余部分就是参数
                    if keyword in ["润色", "改写", "总结"]:
                        tool_info["params"]["text"] = remaining
                    elif keyword == "生成标题":
                        tool_info["params"]["topic"] = remaining
                    elif keyword == "写文章":
                        tool_info["params"]["topic"] = remaining
                else:
                    # 如果没有剩余内容，使用默认占位
                    if keyword in ["润色", "改写", "总结"]:
                        tool_info["params"]["text"] = "默认文案"
                    elif keyword == "生成标题":
                        tool_info["params"]["topic"] = "默认主题"
                    elif keyword == "写文章":
                        tool_info["params"]["topic"] = "默认主题"
                tool_to_call = tool_info
                break
        if tool_to_call:
            tool_name = tool_to_call["tool"]
            tool_params = tool_to_call["params"]
            logger.info(f"关键词匹配到工具: {tool_name}, 参数: {tool_params}")
            tool_prompt = TOOLS[tool_name](**tool_params)
            response2 = await client.chat.completions.create(
                model=config.MODEL,
                messages=[{"role": "user", "content": tool_prompt}],
                )
            ai_reply = response2.choices[0].message.content.strip()
            logger.info(f"工具 {tool_name} 执行完成（兜底）")
        else:
            logger.info("未匹配到任何工具关键词，直接返回")





    user_histories[user_id].append({"role":"assistant","content":ai_reply})
    save_to_db(user_id, user_input, ai_reply) 
    logger.info(f"用户 {user_id} 对话已存入数据库")              #日志
    return ai_reply 


#1. 导入依赖 ✅
#2. 初始化 AsyncOpenAI 客户端 ✅
#3. init_db() 建表 ✅
#4. user_histories 缓存 ✅
#5. chat() 函数：
   #a. 管理历史 ✅
   #b. 第一次调大模型 ✅
   #c. 判断是否调用工具（缩进正确）✅
   #d. 第二次调大模型（在 if 里面）✅
   #e. 更新历史 + 存数据库 ✅
   #f. 返回 ✅