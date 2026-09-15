#main.py
#main.py 同步版vs异步版
#def chat(request:ChatRequest): ------>  async def chat(request:ChatRequest): 
#reply= agent.chat(...)     ------------->     reply= await agent.chat(...)
  


from fastapi import FastAPI
from pydantic import BaseModel

import core.agent
from config import config

from logger import logger        #日志




app=FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION
)
@app.get("/")
def root():
    return {
        "title":f'欢迎使用{config.APP_TITLE}',
        "docs":"/docs",
        "version":config.APP_VERSION
    }




class ChatRequest(BaseModel):
    user_id:str
    user_input:str

@app.post("/chat")
async def chat(request:ChatRequest):
    logger.info(f"收到请求 user_id={request.user_id}")                    #日志
    try:
        reply= await core.agent.chat(request.user_id,request.user_input)
        return {"reply":reply}
    except Exception as e:
        logger.error(f"请求处理异常: {e}")
        return {"reply": "抱歉，处理过程中出现了问题，请稍后再试。"}


if __name__=="__main__":
        import uvicorn
        uvicorn.run("main:app", host=config.API_HOST, port=config.API_PORT, reload=True)    


#查缺补漏：
# 1、防止同一个用户同时发两个请求需加锁