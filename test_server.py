from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
import httpx
import uvicorn
import json
import shutil
import io
import pandas as pd

from config import config

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

        :root {
            --bg: #0a0e1a;
            --panel: #111827;
            --panel-2: #1a2235;
            --border: #1f2a44;
            --text: #e5e9f0;
            --text-dim: #8892a8;
            --accent: #00d4ff;
            --accent-dim: #0891b2;
            --user: #0ea5e9;
        }

        body {
            font-family: "SF Mono", "JetBrains Mono", "Consolas", -apple-system, sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-image:
                radial-gradient(circle at 20% 0%, rgba(0, 212, 255, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 80% 100%, rgba(139, 92, 246, 0.06) 0%, transparent 50%);
        }

        .container {
            width: 100%;
            max-width: 760px;
            height: 85vh;
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 0 60px rgba(0, 212, 255, 0.06);
        }

        .header {
            padding: 18px 24px;
            background: linear-gradient(180deg, var(--panel-2) 0%, var(--panel) 100%);
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header-title h1 {
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 1px;
            color: var(--text);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .header-title h1::before {
            content: "";
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 8px var(--accent);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }

        .header-title p {
            font-size: 11px;
            color: var(--text-dim);
            margin-top: 4px;
            letter-spacing: 0.5px;
            padding-left: 16px;
        }

        .header-actions { display: flex; gap: 8px; }

        .upload-btn {
            padding: 7px 14px;
            background: var(--panel-2);
            color: var(--text-dim);
            border: 1px solid var(--border);
            border-radius: 6px;
            font-size: 12px;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.2s;
            letter-spacing: 0.5px;
        }

        .upload-btn:hover {
            color: var(--accent);
            border-color: var(--accent);
            box-shadow: 0 0 12px rgba(0, 212, 255, 0.2);
        }

        .chat {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .msg {
            display: flex;
            gap: 12px;
            max-width: 88%;
            animation: fadeIn 0.4s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .msg.user { align-self: flex-end; flex-direction: row-reverse; }

        .avatar {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 14px;
            flex-shrink: 0;
            border: 1px solid var(--border);
            background: var(--panel-2);
        }

        .msg.user .avatar {
            color: var(--user);
            border-color: rgba(14, 165, 233, 0.3);
            background: rgba(14, 165, 233, 0.08);
        }

        .msg.ai .avatar {
            color: var(--accent);
            border-color: rgba(0, 212, 255, 0.3);
            background: rgba(0, 212, 255, 0.08);
        }

        .bubble {
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.7;
            white-space: pre-wrap;
            word-break: break-word;
        }

        .msg.user .bubble {
            background: rgba(14, 165, 233, 0.12);
            border: 1px solid rgba(14, 165, 233, 0.25);
            color: var(--text);
        }

        .msg.ai .bubble {
            background: var(--panel-2);
            border: 1px solid var(--border);
            color: var(--text);
        }

        .bubble .cursor {
            display: inline-block;
            width: 7px;
            height: 14px;
            background: var(--accent);
            margin-left: 3px;
            vertical-align: text-bottom;
            animation: blink 1s infinite;
            box-shadow: 0 0 6px var(--accent);
        }

        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }

        .input-area {
            padding: 16px 20px;
            background: var(--panel-2);
            border-top: 1px solid var(--border);
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .input-area input {
            flex: 1;
            padding: 12px 16px;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
            font-family: inherit;
            color: var(--text);
            outline: none;
            transition: all 0.2s;
        }

        .input-area input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.1);
        }

        .input-area input::placeholder { color: var(--text-dim); }

        .input-area button {
            padding: 12px 24px;
            background: var(--accent);
            color: var(--bg);
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            font-family: inherit;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.2s;
        }

        .input-area button:hover:not(:disabled) {
            background: #33ddff;
            box-shadow: 0 0 20px rgba(0, 212, 255, 0.4);
        }

        .input-area button:disabled {
            opacity: 0.3;
            cursor: not-allowed;
        }

        .chat::-webkit-scrollbar { width: 6px; }
        .chat::-webkit-scrollbar-thumb {
            background: var(--border);
            border-radius: 3px;
        }
        .chat::-webkit-scrollbar-thumb:hover { background: var(--accent-dim); }
        .chat::-webkit-scrollbar-track { background: transparent; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-title">
                <h1>AI 文案助手</h1>
                <p>生成标题 · 撰写文章 · 润色总结 · 数据分析</p>
            </div>
            <div class="header-actions">
                <button class="upload-btn" onclick="document.getElementById('excelInput').click()">📊 导入</button>
                <button class="upload-btn" onclick="downloadExcel()">📥 导出</button>
                <button class="upload-btn" onclick="downloadViral()">📥 导出爆文</button>
            </div>
            <input type="file" id="excelInput" accept=".xlsx,.xls" style="display:none" onchange="uploadExcel()">
        </div>
        <div class="chat" id="chat">
            <div class="msg ai">
                <div class="avatar">🤖</div>
                <div class="bubble">你好！我是你的文案助手 ✨<br><br>💡 输入 <b>/history</b> 查看历史记录<br>🗑️ 输入 <b>/delete</b> 清空历史记录<br>📊 右上角导入 / 导出 Excel<br>📈 说"<b>分析一下数据</b>"查看运营分析<br><br>或者直接告诉我你想做什么～</div>
            </div>
        </div>
        <div class="input-area">
            <input id="input" placeholder="输入你的需求..." autofocus>
            <button id="send" onclick="send()">发送</button>
        </div>
    </div>

    <script>
        let userId = localStorage.getItem('chat_user_id');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substring(2, 10) + Date.now().toString(36);
            localStorage.setItem('chat_user_id', userId);
        }
        const chat = document.getElementById("chat");
        const input = document.getElementById("input");
        const sendBtn = document.getElementById("send");
        const AUTH_KEY = "__AUTH_KEY__";

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
                    headers: {"Content-Type": "application/json", "X-Auth-Key": AUTH_KEY},
                    body: JSON.stringify({user_id: userId, user_input: text})
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

        async function uploadExcel() {
            const fileInput = document.getElementById('excelInput');
            const file = fileInput.files[0];
            if (!file) return;
            const bubble = addMsg("ai");
            bubble.innerHTML = "📊 正在导入，请稍候...";
            const formData = new FormData();
            formData.append("file", file);
            try {
                const resp = await fetch("/upload_own_articles", {
                    method: "POST",
                    headers: {"X-Auth-Key": AUTH_KEY},
                    body: formData
                });
                const result = await resp.json();
                if (resp.ok) {
                    bubble.innerHTML = `✅ ${result.msg}`;
                } else {
                    bubble.innerHTML = `❌ 导入失败：${result.detail || "未知错误"}`;
                }
            } catch (e) {
                bubble.innerHTML = `❌ 上传出错：${e.message}`;
            }
            fileInput.value = "";
            chat.scrollTop = chat.scrollHeight;
        }

        async function downloadExcel() {
            const bubble = addMsg("ai");
            bubble.innerHTML = "📥 正在导出...";
            try {
                const resp = await fetch("/export_own_articles", {
                    method: "GET",
                    headers: {"X-Auth-Key": AUTH_KEY}
                });
                if (!resp.ok) { bubble.innerHTML = "❌ 导出失败"; return; }
                const blob = await resp.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "own_articles_export.xlsx";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                bubble.innerHTML = "✅ 导出成功，请查看下载文件夹";
            } catch (e) {
                bubble.innerHTML = `❌ 导出出错：${e.message}`;
            }
            chat.scrollTop = chat.scrollHeight;
        }

        async function downloadViral() {
            const bubble = addMsg("ai");
            bubble.innerHTML = "📥 正在导出爆文...";
            try {
                const resp = await fetch("/export_viral", {
                    method: "GET",
                    headers: {"X-Auth-Key": AUTH_KEY}
                });
                if (!resp.ok) { bubble.innerHTML = "❌ 导出失败"; return; }
                const blob = await resp.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "viral_articles_export.xlsx";
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                bubble.innerHTML = "✅ 爆文导出成功，请查看下载文件夹";
            } catch (e) {
                bubble.innerHTML = `❌ 导出出错：${e.message}`;
            }
            chat.scrollTop = chat.scrollHeight;
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
    return HTMLResponse(HTML.replace("__AUTH_KEY__", config.AUTH_KEY))


@app.post("/chat_stream")
async def proxy(request: Request):
    body = await request.body()

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


# ===== 上传自己的文章 =====
@app.post("/upload_own_articles")
async def upload_own_articles(file: UploadFile = File(...)):
    tmp_path = "temp_upload.xlsx"
    with open(tmp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    from content.import_excel import import_from_excel
    try:
        import_from_excel(tmp_path)
        return {"msg": "Excel 导入成功"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"detail": f"导入失败：{str(e)}"}
        )


# ===== 导出自己的文章 =====
@app.get("/export_own_articles")
async def export_own_articles():
    from config import get_conn
    conn = get_conn()
    df = pd.read_sql("""
        SELECT id, title, content, platform, publish_date,
               views, likes, collects, comments, shares, followers_gained
        FROM own_articles
        ORDER BY id DESC
    """, conn)
    conn.close()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="own_articles")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=own_articles_export.xlsx"}
    )


# ===== 导出爆文 =====
@app.get("/export_viral")
async def export_viral():
    from config import get_conn
    conn = get_conn()
    df = pd.read_sql("""
        SELECT id, title, content, author, author_followers,
               platform, note_url, likes, collects, comments, collected_date
        FROM viral_articles
        ORDER BY id DESC
    """, conn)
    conn.close()

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="viral_articles")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=viral_articles_export.xlsx"}
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5500)