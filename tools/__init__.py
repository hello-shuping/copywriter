from .generate_title import generate_title
from .write_article import write_article
from .polish import polish
from .summarize import summarize
from .analyze_stats import analyze_stats

TOOLS = {
    "generate_title" : generate_title,
    "write_article" : write_article,
    "polish" : polish,
    "summarize" : summarize,
    "analyze_stats": analyze_stats,
    }

