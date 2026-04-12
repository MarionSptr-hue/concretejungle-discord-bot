import requests
from bs4 import BeautifulSoup
import os
import json

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

url = "https://concretejungle.forumactif.com/f11-roll-call"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "html.parser")

topics = soup.select("a.topictitle")

try:
    with open("posted.json", "r") as f:
        posted = json.load(f)
except:
    posted = []

new_posts = []

for topic in topics:
    try:
        title = topic.text.strip()
        link = "https://concretejungle.forumactif.com" + topic["href"]

        if link not in posted:
            new_posts.append({
                "title": title,
                "link": link
            })

    except:
        continue


for post in reversed(new_posts):

    data = {
        "content": f"📢 @everyone\n\nUn nouveau visage apparaît dans la jungle...\n\n📝 {post['title']}\n\nVenez lui souhaiter la bienvenue :\n{post['link']}"
    }

    requests.post(WEBHOOK, json=data)

    posted.append(post["link"])


with open("posted.json", "w") as f:
    json.dump(posted, f)
       
