#agent.py
#agent.py 同步版vs异步版 
#from openai import OpenAI ------->  from openai import AsyncOpenAI
#client = OpenAI(...)     ---------->      client = AsyncOpenAI(...)
#def chat(user_input):    ---------->      async def chat(user_input):
#response = client.chat.... -----> response = await client.chat...   



from openai import AsyncOpenAI
from config import config 
from db.ccs import init_db,save_to_db


client = AsyncOpenAI(
    api_key = config.API_KEY,
    base_url=config.BASE_URL
    )


init_db()


user_histories={} #字典

async def chat(user_id,user_input):
    if user_id not in user_histories:
        user_histories[user_id]=[{"role":"system","content":config.SYSTEM_PROMPT}]
    user_histories[user_id].append({"role":"user","content":user_input})
    response = await client.chat.completions.create(
        model=config.MODEL,
        messages=user_histories[user_id],  #列表
        )
    ai_reply=response.choices[0].message.content
    user_histories[user_id].append({"role":"assistant","content":ai_reply})

    save_to_db(user_id, user_input, ai_reply) 

    return ai_reply 


