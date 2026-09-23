TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "polish",
            "description": "润色文案",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "原文",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["正式", "轻松", "小红书", "简洁"],
                        "description": "风格，默认正式",
                    },
                },
                "required": ["text", "style"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "generate_title",
            "description": "生成标题",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "主题",
                    },
                    "count": {
                        "type": "integer",
                        "description": "生成数量，如果用户没有明确指定，默认填 3",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["正式", "轻松", "专业", "故事感", "干货型"],
                        "description": "风格，默认正式",
                    },
                },
                "required": ["topic", "count", "style"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "write_article",
            "description": "写文章",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "主题",
                    },
                    "word_count": {
                        "type": "integer",
                        "description": "字数，默认1200",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["正式", "轻松", "专业", "故事感", "口语化"],
                        "description": "风格，默认正式",
                    },
                },
                "required": ["topic", "word_count", "style"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "summarize",
            "description": "总结内容",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "原文",
                    },
                    "length": {
                        "type": "string",
                        "enum": ["简短", "详细"],
                        "description": "长度，默认简短",
                    },
                },
                "required": ["text", "length"],
                "additionalProperties": False,
            },
        },
    },
]