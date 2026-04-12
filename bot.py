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
        title_elem = topic.select_one(".topictitle")

        if not title_elem:
            continue

        link = "https://concretejungle.forumactif.com" + title_elem["href"]

        author_elem = topic.select_one(".lastpost strong a")

        if author_elem:
            author = author_elem.text.strip()
        else:
            author = "Nouveau membre"

        if link not in posted:
            new_posts.append({
                "author": author,
                "link": link
            })

    except:
        continue


# On envoie toutes les nouvelles fiches
for post in reversed(new_posts):

    data = {
        "content": f"📢 @everyone\n\nUn nouveau visage apparaît dans la jungle...\n\n👤 {post['author']}\n\nVenez lui souhaiter la bienvenue :\n{post['link']}"
    }

    requests.post(WEBHOOK, json=data)

    posted.append(post["link"])


# On sauvegarde l'historique
with open("posted.json", "w") as f:
    json.dump(posted, f)
