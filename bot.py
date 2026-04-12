import requests
from bs4 import BeautifulSoup
import os
import json

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

url = "https://concretejungle.forumactif.com/f11-roll-call"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

topics = soup.select(".topiclist.topics li")

try:
    with open("posted.json", "r") as f:
        posted = json.load(f)
except:
    posted = []

new_posts = []

for topic in topics:

    classes = topic.get("class", [])

    if "sticky" in classes or "announce" in classes:
        continue

    try:
        title = topic.select_one(".topictitle").text.strip()
        link = "https://concretejungle.forumactif.com" + topic.select_one(".topictitle")["href"]
        author = topic.select_one(".lastpost strong a").text.strip()

        if link not in posted:
            new_posts.append({
                "author": author,
                "link": link
            })

    except:
        continue


new_posts.reverse()

for post in new_posts:

    data = {
        "content": f"📢 @everyone\n\nUn nouveau visage apparaît dans les rues de Londres...\n\n👤 {post['author']}\n\nVenez lui souhaiter la bienvenue :\n{post['link']}"
    }

    requests.post(WEBHOOK, json=data)

    posted.append(post["link"])


with open("posted.json", "w") as f:
    json.dump(posted, f)

    with open("last_post.txt", "w") as f:
        f.write(link)
