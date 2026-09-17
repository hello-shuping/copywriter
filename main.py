# main.py

from fastapi import FastAPI,Header,HTTPException,Depends #API_KEY鉴权
from pydantic import BaseModel
from fastapi.responses import StreamingResponse

import agent
from config import config
from logger import logger


app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION,
    version=config.APP_VERSION
)

async def verify_key(x_auth_key: str = Header(...)):  #API_KEY鉴权
    if not config.AUTH_KEY:
        raise HTTPException(status_code=503, detail="服务未开放")
    if x_auth_key != config.AUTH_KEY:
        raise HTTPException(status_code=401, detail="Invalid Auth Key")
    
@app.get("/")
def root():
    return {
        "title": f"欢迎使用{config.APP_TITLE}",
        "docs": "/docs",
        "version": config.APP_VERSION
    }
@app.get("/health")
async def health():
    return {"status": "ok"}





class ChatRequest(BaseModel):
    user_id: str
    user_input: str


@app.post("/chat_stream")
async def chat_stream(
    request: ChatRequest,
    _: str = Depends(verify_key),   #API_KEY鉴权
):
    if len(request.user_input) > config.MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=413,
            detail=f"输入过长，最多 {config.MAX_INPUT_LENGTH} 字"
        )
    logger.info(f"收到请求 user_id={request.user_id}")
    return StreamingResponse(
        agent.chat_stream(request.user_id, request.user_input),
        media_type="text/plain"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=False
    )