#main.py
#main.py 同步版vs异步版
#def chat(request:ChatRequest): ------>  async def chat(request:ChatRequest): 
#reply= agent.chat(...)     ------------->     reply= await agent.chat(...)
  


from fastapi import FastAPI
from pydantic import BaseModel

import core.agent
from config import config


app=FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION
)


class ChatRequest(BaseModel):
    user_id:str
    user_input:str


@app.get("/")
def root():
    return {
        "title":f'欢迎使用{config.APP_TITLE}',
        "docs":"/docs",
        "version":config.APP_VERSION
    }


@app.post("/chat")
async def chat(request:ChatRequest):
    reply= await core.agent.chat(request.user_id,request.user_input)
    return {"reply":reply}


if __name__=="__main__":
        import uvicorn
        uvicorn.run("main:app", host=config.API_HOST, port=config.API_PORT, reload=True)    


#查缺补漏：
# 1、防止同一个用户同时发两个请求需加锁