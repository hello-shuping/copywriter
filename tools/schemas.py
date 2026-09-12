TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "polish",
            "description": "润色文案，把一段文字改得更通顺、更有质感",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "需要润色的原文",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["正式", "轻松", "小红书", "简洁"],
                        "description": "目标风格。用户没有明确说'轻松/小红书/简洁'时，必须填「正式」",
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
            "description": "根据主题生成多个标题",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "标题的主题",
                    },
                    "count": {
                        "type": "integer",
                        "description": "生成数量，如果用户没有明确指定，默认填 5",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["正式", "轻松", "专业", "故事感", "干货型"],
                        "description": "风格，如果用户没有明确指定，默认填「正式」",
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
            "description": "根据主题写一篇完整文章",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "文章主题",
                    },
                    "word_count": {
                        "type": "integer",
                        "description": "目标字数，如果用户没有明确指定，默认填 1200",
                    },
                    "style": {
                        "type": "string",
                        "enum": ["正式", "轻松", "专业", "故事感", "口语化"],
                        "description": "风格，如果用户没有明确指定，默认填「正式」",
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
            "description": "总结一段内容",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "需要总结的原文",
                    },
                    "length": {
                        "type": "string",
                        "enum": ["简短", "详细"],
                        "description": "总结长度，如果用户没有明确指定，默认填「简短」",
                    },
                },
                "required": ["text", "length"],
                "additionalProperties": False,
            },
        },
    },
]