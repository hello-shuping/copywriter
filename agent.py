# agent.py

import json
from openai import AsyncOpenAI

from config import config
from db.ccs import init_db, save_to_db, load_history,clear_history
from tools import TOOLS
from tools.schemas import TOOL_SCHEMAS
from logger import logger


client = AsyncOpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

init_db()

user_history = {}


async def chat_stream(user_id, user_input):
    # ===== 命令：查看历史 =====
    if user_input.strip().lower() == "/history":
        if user_id not in user_history:
            user_history[user_id] = load_history(user_id, 5, config.SYSTEM_PROMPT)
        messages = user_history[user_id]
        lines = []
        for m in messages:
            if m["role"] == "user":
                lines.append(f"你：{m['content']}")
            elif m["role"] == "assistant":
                lines.append(f"AI：{m['content']}")
        yield "\n".join(lines) if lines else "暂无历史记录"
        return

    # ===== 命令：清空历史 =====
    if user_input.strip().lower() == "/delete":
        clear_history(user_id)
        user_history[user_id] = [
            {"role": "system", "content": config.SYSTEM_PROMPT}
        ]
        yield "已清空历史记录"
        return
    # ===========================


    try:
        # 1. 加载/更新历史
        if user_id not in user_history:
            user_history[user_id] = load_history(user_id, 5, config.SYSTEM_PROMPT)
            logger.info(f"用户 {user_id} 加载历史，共 {len(user_history[user_id])} 条消息")

        user_history[user_id].append({"role": "user", "content": user_input})

        # 2. 第一次调用大模型 —— 流式
        response = await client.chat.completions.create(
            model=config.MODEL,
            messages=user_history[user_id],
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            stream=True,
        )

        content = ""
        tool_calls_buffer = {}

        async for chunk in response:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta

            # 普通文本：边收边吐
            if delta.content:
                content += delta.content
                yield delta.content

            # 工具调用分片：先累积
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in tool_calls_buffer:
                        tool_calls_buffer[idx] = {"name": "", "arguments": ""}
                    if tc.function and tc.function.name:
                        tool_calls_buffer[idx]["name"] += tc.function.name
                    if tc.function and tc.function.arguments:
                        tool_calls_buffer[idx]["arguments"] += tc.function.arguments
                        
        # 3. 判断是否有工具调用
        if tool_calls_buffer:
            tc = tool_calls_buffer[0]
            tool_name = tc["name"]
            tool_args = json.loads(tc["arguments"])
            logger.info(f"检测到工具调用: {tool_name}, 参数: {tool_args}")

            # 执行工具，拿到 prompt
            tool_prompt = TOOLS[tool_name](**tool_args)

            # 4. 第二次调用大模型 —— 流式
            response2 = await client.chat.completions.create(
                model=config.MODEL,
                messages=[{"role": "user", "content": tool_prompt}],
                stream=True,
            )

            ai_reply = ""
            async for chunk in response2:
                if chunk.choices[0].delta.content:
                    ai_reply += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content

            logger.info(f"工具 {tool_name} 执行完成")
            user_history[user_id].append({"role": "assistant", "content": ai_reply})
            save_to_db(user_id, user_input, ai_reply)
        else:
            # 5. 没有工具调用：content 已经边收边吐了
            logger.info("未检测到工具调用，直接返回")
            user_history[user_id].append({"role": "assistant", "content": content})
            save_to_db(user_id, user_input, content)
    except Exception as e:
        logger.error(f"流式异常: {e}")
        yield "抱歉，服务暂时不可用，请稍后再试。"