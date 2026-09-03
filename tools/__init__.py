from .generate_title import generate_title
from .write_article import write_article
from .polish import polish
from .summarize import summarize


TOOLS = {
    "generate_title" : generate_title,
    "write_article" : write_article,
    "polish" : polish,
    "summarize" : summarize
    }

TOOLS_DESCRIPTION = """
    -generate_title: 生成标题, 参数 topic(主题),count(数量),style(正式/轻松/专业/故事感/干货型)
    -write_article: 撰写文章, 参数 topic(主题),word_count(字数), style(正式/轻松/专业/故事感)
    -polish: 润色文案, 参数 text(原文), style(正式/轻松/简洁/小红书)
    -summarize: 总结内容, 参数 text(原文), length(简短/详细)
"""

