import urllib.request
import json

with open("article.txt", "r", encoding="utf-8") as f:
    article = f.read()

data = json.dumps({
    "user_id": "string",
    "user_input": "总结一下：" + article
}).encode("utf-8")

req = urllib.request.Request(
    "http://localhost:8000/chat",
    data=data,
    headers={"Content-Type": "application/json"}
)

with urllib.request.urlopen(req) as resp:
    print(json.loads(resp.read().decode("utf-8")))