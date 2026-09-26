# copywriter · AI 文案助手

基于 FastAPI + PostgreSQL + LLM 的 AI 文案助手，支持流式对话、多轮记忆、Function Calling、数据分析和爆文检索。

## 功能

- **文案生成**：生成标题、撰写文章、润色、总结（Function Calling 工具调用）
- **爆文检索**：红狐 API 自动爬取小红书爆文，生成时参考爆款风格
- **数据分析**：互动率排名、标题规律分析、创作建议
- **流式对话**：基于 SSE 逐字返回，工具调用也支持流式
- **多轮记忆**：按 user_id 维护上下文，存 PostgreSQL，重启不丢
- **数据管理**：Excel 批量导入导出、会话管理（/history、/delete）
- **接口鉴权**：API Key 鉴权 + 请求长度限制

## 技术栈

| 类别 | 技术 |
|------|------|
| 语言 | Python 3.14 |
| Web 框架 | FastAPI + Uvicorn |
| 大模型 | 千问 qwen-plus（OpenAI 兼容接口） |
| Embedding | 千问 text-embedding-v4（1024维） |
| 数据库 | PostgreSQL + pgvector |
| 爆文数据 | 红狐数据 API |
| 数据处理 | pandas + openpyxl |
| 工具调用 | Function Calling（标准 tools 参数） |

## 架构设计

| 层 | 文件 | 职责 |
|----|------|------|
| 用户层 | test_server.py | 聊天界面、导入导出 |
| 路由层 | main.py | 鉴权、校验、转发 |
| 服务层 | agent.py | 编排流程、判断意图、调工具 |
| 工具层 | tools/ | 每个工具的具体实现 |
| 数据层 | content/、db/ | 数据存取、Excel 导入、分析 |
| AI 适配层 | 客户端封装 | 千问对话、千问 Embedding、红狐 |
| 存储层 | PostgreSQL | 数据持久化 |

**核心设计：服务层只管编排，工具层只管实现，数据层只管存取。加新工具不改核心代码。**

## 数据流

### 对话链路

用户输入 → 鉴权 → 加载历史 → 第1次调大模型 → 执行工具 → 第2次调大模型 → 存数据库

### 导入链路

Excel 上传 → pandas 解析 → 逐篇转向量 → 存进 own_articles

### 检索链路

用户问题 → 转向量 → pgvector 相似度检索 → 按点赞重排 → 拼进 prompt 参考

### 爬取链路

红狐 API → 搜索小红书爆文 → 转向量 → 存进 viral_articles

## 项目结构

copywriter/
├── main.py
├── agent.py
├── config.py
├── logger.py
├── test_server.py
├── requirements.txt
├── .env
├── .env.example
├── content/
│   ├── __init__.py
│   ├── own.py
│   ├── viral.py
│   ├── redfox.py
│   └── import_excel.py
├── db/
│   ├── __init__.py
│   └── ccs.py
├── tools/
│   ├── __init__.py
│   ├── schemas.py
│   ├── polish.py
│   ├── generate_title.py
│   ├── write_article.py
│   ├── summarize.py
│   └── analyze_stats.py
├── tests/
│   ├── __init__.py
│   └── test_tools.py
└── logs/

## 快速开始

pip install -r requirements.txt
python main.py

浏览器访问 http://localhost:8000，接口文档 /docs。

## 环境变量

API_KEY=sk-xxx
BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
MODEL=qwen-plus

EMBEDDING_API_KEY=sk-xxx
EMBEDDING_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
EMBEDDING_MODEL=text-embedding-v4

REDFOX_API_KEY=ak_xxx
AUTH_KEY=你自己编的密钥

DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=postgres
DB_USER=postgres
DB_PASSWORD=你的密码

## 接口说明

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /chat_stream | 流式对话 |
| GET | /history | 查历史 |
| DELETE | /history | 清空历史 |
| GET | /health | 健康检查 |

## 添加新工具

1. 新建 tools/your_tool.py
2. 在 tools/__init__.py 注册到 TOOLS 字典
3. 在 tools/schemas.py 加 Function Calling 定义

## License

MIT
