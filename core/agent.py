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


client = AsyncOpenAI(
    api_key = config.API_KEY,
    base_url=config.BASE_URL
    )

init_db()

user_histories={} #字典

async def chat(user_id,user_input):
    if user_id not in user_histories:
        user_histories[user_id]=[
            {"role":"system","content":"你是一个智能助手，可以根据用户需求调用工具。如果用户需要工具，返回 JSON 格式：{\"tool\": \"工具名\", \"params\": {...}}。如果用户只是闲聊，直接回复聊天内容。"}
            ]
    user_histories[user_id].append({"role":"user","content":user_input})



    #第1次调用大模型
    response = await client.chat.completions.create(
        model=config.MODEL,
        messages=user_histories[user_id],  #列表
        )
    ai_reply=response.choices[0].message.content
    #判断是否使用工具
    if ai_reply.startswith("{") and "tool" in ai_reply:
        data=json.loads(ai_reply)
        tool_name = data["tool"]
        tool_params = data["params"]

        tool_prompt = TOOLS[tool_name](**tool_params)
    #第2次调用大模型
        response2 = await client.chat.completions.create(
        model=config.MODEL,
        messages=[{"role": "user", "content": tool_prompt}],  
        )
        ai_reply=response2.choices[0].message.content    



    user_histories[user_id].append({"role":"assistant","content":ai_reply})
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