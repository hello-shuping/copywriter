#agent.py
#agent.py 同步版vs异步版 
#from openai import OpenAI ------->  from openai import AsyncOpenAI
#client = OpenAI(...)     ---------->      client = AsyncOpenAI(...)
#def chat(user_input):    ---------->      async def chat(user_input):
#response = client.chat.... -----> response = await client.chat...   


from openai import AsyncOpenAI
from config import config 
from db.ccs import init_db,save_to_db,load_history
import json
from tools import TOOLS
from tools.schemas import TOOL_SCHEMAS
from logger import logger


client = AsyncOpenAI(
    api_key = config.API_KEY,
    base_url=config.BASE_URL
    )

init_db()

user_history={} #字典

async def chat(user_id,user_input):
    if user_id not in user_history:
        user_history[user_id] = load_history(user_id, 20, config.SYSTEM_PROMPT)
        logger.info(f"用户 {user_id} 加载历史，共 {len(user_history[user_id])} 条消息")   # ← 加日志

    user_history[user_id].append({"role":"user","content":user_input})


    #第1次调用大模型
    response = await client.chat.completions.create(
        model=config.MODEL,
        messages=user_history[user_id],                #列表
        tools=TOOL_SCHEMAS,
        tool_choice="auto",
        )
    msg = response.choices[0].message          # 拿到 message 对象
    
    logger.debug(f"第1次返回 - content: {msg.content}")
    logger.debug(f"第1次返回 - tool_calls: {msg.tool_calls}")

    #判断是否使用工具
    if msg.tool_calls:
        tool_call = msg.tool_calls[0]
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments)

        logger.info(f"检测到工具调用: {tool_name}, 参数: {tool_args}")   # ← 加日志

    #执行工具，拿到 prompt
        tool_prompt = TOOLS[tool_name](**tool_args)
    #第2次调用大模型
        response2 = await client.chat.completions.create(
            model=config.MODEL,
            messages=[{"role": "user", "content": tool_prompt}],  
            )
        ai_reply = response2.choices[0].message.content    
        logger.info(f"工具 {tool_name} 执行完成，结果: {ai_reply}")   # ← 加日志
    else:
        ai_reply = msg.content
        logger.info("未检测到工具调用，直接返回")     # ← 加日志

    user_history[user_id].append({"role":"assistant","content":ai_reply})
    save_to_db(user_id, user_input, ai_reply) 
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