import requests
from bs4 import BeautifulSoup
import os

WEBHOOK = os.getenv("DISCORD_WEBHOOK")

url = "https://concretejungle.forumactif.com/f11-roll-call"

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

topics = soup.select(".topiclist.topics li")

valid_topic = None

for topic in topics:
    if "sticky" in topic.get("class", []) or "announce" in topic.get("class", []):
        continue
    
    valid_topic = topic
    break

title = valid_topic.select_one(".topictitle").text.strip()
link = "https://concretejungle.forumactif.com" + valid_topic.select_one(".topictitle")["href"]

author = valid_topic.select_one(".lastpost strong a").text.strip()

try:
    with open("last_post.txt", "r") as f:
        last_post = f.read().strip()
except:
    last_post = None

if last_post is None:
    with open("last_post.txt", "w") as f:
        f.write(link)

elif link != last_post:

    data = {
        "content": f"📢 @everyone\n\nUn nouveau visage apparaît dans les rues de Londres...\n\n👤 {author}\n\nVenez lui souhaiter la bienvenue :\n{link}"
    }

    requests.post(WEBHOOK, json=data)

    with open("last_post.txt", "w") as f:
        f.write(link)
