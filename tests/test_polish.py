# test_polish.py
from tools.polish import polish
def test_polish_style():
    result = polish("这个产品不错","搞笑")
    assert "正式" in result

