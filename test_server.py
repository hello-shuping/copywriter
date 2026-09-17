from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
import httpx
import uvicorn
import json

app = FastAPI()

HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 文案助手</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 720px;
            height: 85vh;
            background: #fff;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }
        .header {
            padding: 20px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
        }
        .header h1 { font-size: 18px; font-weight: 600; }
        .header p { font-size: 13px; opacity: 0.85; margin-top: 4px; }
        .chat {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 16px;
            background: #f7f8fc;
        }
        .msg {
            display: flex;
            gap: 10px;
            max-width: 85%;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .msg.user { align-self: flex-end; flex-direction: row-reverse; }
        .avatar {
            width: 36px; height: 36px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 16px;
            flex-shrink: 0;
        }
        .msg.user .avatar { background: #667eea; color: #fff; }
        .msg.ai .avatar { background: #e8eaf6; color: #667eea; }
        .bubble {
            padding: 12px 16px;
            border-radius: 14px;
            font-size: 15px;
            line-height: 1.6;
            white-space: pre-wrap;
            word-break: break-word;
        }
        .msg.user .bubble {
            background: #667eea;
            color: #fff;
            border-bottom-right-radius: 4px;
        }
        .msg.ai .bubble {
            background: #fff;
            color: #333;
            border-bottom-left-radius: 4px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        .bubble .cursor {
            display: inline-block;
            width: 8px;
            height: 16px;
            background: #667eea;
            margin-left: 2px;
            vertical-align: text-bottom;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        .input-area {
            padding: 16px 20px;
            background: #fff;
            border-top: 1px solid #eee;
            display: flex;
            gap: 10px;
        }
        .input-area input {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #e0e0e0;
            border-radius: 24px;
            font-size: 15px;
            outline: none;
            transition: border-color 0.2s;
        }
        .input-area input:focus { border-color: #667eea; }
        .input-area button {
            padding: 0 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            border: none;
            border-radius: 24px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .input-area button:hover:not(:disabled) {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .input-area button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        .chat::-webkit-scrollbar { width: 6px; }
        .chat::-webkit-scrollbar-thumb {
            background: #ccc;
            border-radius: 3px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✨ AI 文案助手</h1>
            <p>润色 · 生成标题 · 写文章 · 总结</p>
        </div>
        <div class="chat" id="chat">
            <div class="msg ai">
                <div class="avatar">🤖</div>
                <div class="bubble">你好！我是你的文案助手 ✨<br><br>💡 输入 <b>/history</b> 查看历史记录<br>🗑️ 输入 <b>/delete</b> 清空历史记录<br><br>或者直接告诉我你想做什么～</div>
            </div>
        </div>
        <div class="input-area">
            <input id="input" placeholder="输入你的需求..." autofocus>
            <button id="send" onclick="send()">发送</button>
        </div>
    </div>

    <script>
        const chat = document.getElementById("chat");
        const input = document.getElementById("input");
        const sendBtn = document.getElementById("send");

        function addMsg(role, text = "") {
            const msg = document.createElement("div");
            msg.className = "msg " + role;
            const avatar = role === "user" ? "👤" : "🤖";
            msg.innerHTML = `
                <div class="avatar">${avatar}</div>
                <div class="bubble">${text}<span class="cursor"></span></div>
            `;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
            return msg.querySelector(".bubble");
        }

        async function send() {
            const text = input.value.trim();
            if (!text) return;

            input.value = "";
            sendBtn.disabled = true;

            addMsg("user", text).querySelector(".cursor").remove();

            const bubble = addMsg("ai");

            try {
                const response = await fetch("/chat_stream", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-Auth-Key": "3d9aaa239852fa5466cbd45d252244e3b267f33d690f8519bb17e70102768bb0"
                    },
                    body: JSON.stringify({user_id: "u001", user_input: text})
                });

                if (!response.ok) {
                    const err = await response.json();
                    bubble.innerHTML = err.detail || "请求失败";
                    sendBtn.disabled = false;
                    input.focus();
                    return;
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let fullText = "";

                while (true) {
                    const {done, value} = await reader.read();
                    if (done) break;
                    fullText += decoder.decode(value);
                    bubble.innerHTML = fullText.replace(/\\n/g, "<br>") + '<span class="cursor"></span>';
                    chat.scrollTop = chat.scrollHeight;
                }

                bubble.innerHTML = fullText.replace(/\\n/g, "<br>");
            } catch (e) {
                bubble.innerHTML = "抱歉，出错了：" + e.message;
            }

            sendBtn.disabled = false;
            input.focus();
        }

        input.addEventListener("keydown", e => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                send();
            }
        });
    </script>
</body>
</html>
"""


@app.get("/")
async def index():
    return HTMLResponse(HTML)


@app.post("/chat_stream")
async def proxy(request: Request):
    body = await request.body()

    # 代理层长度检查
    try:
        data = json.loads(body)
        if len(data.get("user_input", "")) > 2000:
            return JSONResponse(
                status_code=413,
                content={"detail": "输入过长，最多 2000 字"}
            )
    except:
        pass

    auth_key = request.headers.get("X-Auth-Key", "")

    async def stream_generator():
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                "http://localhost:8000/chat_stream",
                content=body,
                headers={
                    "Content-Type": "application/json",
                    "X-Auth-Key": auth_key,
                },
            ) as resp:
                async for chunk in resp.aiter_raw():
                    yield chunk

    return StreamingResponse(stream_generator(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500)