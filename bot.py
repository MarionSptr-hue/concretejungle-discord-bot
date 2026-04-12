import requests
from bs4 import BeautifulSoup
import os
import json

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

url = "https://concretejungle.forumactif.com/f11-roll-call"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

topic = soup.select_one(".topictitle")

title = topic.text.strip()
link = "https://concretejungle.forumactif.com" + topic["href"]

try:
    with open("last_post.txt", "r") as f:
        last_post = f.read().strip()
except:
    last_post = ""

if link != last_post:

    data = {
        "content": f"📢 @everyone\n\nUn nouveau visage apparaît dans la jungle...\n\n👤 {title}\n\nVenez lui souhaiter la bienvenue :\n{link}"
    }

    requests.post(WEBHOOK, json=data)

    with open("last_post.txt", "w") as f:
        f.write(link)
