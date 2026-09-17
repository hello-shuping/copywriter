# test_polish.py
from tools.generate_title import generate_title
from tools.write_article import write_article
from tools.polish import polish
from tools.summarize import summarize

def test_generate_title_style():
    resule = generate_title


def test_polish_style():
    result = polish("这个产品不错","搞笑")
    assert "正式" in result



