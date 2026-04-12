import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1492657635059830835

last_post = None

async def check_forum():
    global last_post
    await bot.wait_until_ready()

    while not bot.is_closed():
        try:
            url = "https://concretejungle.forumactif.com/f11-roll-call"
            
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "html.parser")

            topic = soup.select_one(".topictitle")

            if topic:
                title = topic.text.strip()
                link = "https://concretejungle.forumactif.com" + topic["href"]

                if last_post != link:
                    last_post = link
                    
                    channel = bot.get_channel(CHANNEL_ID)

                    await channel.send(
                        f"📢 @everyone\n\n"
                        f"Un nouveau visage apparaît dans les rues de Londres...\n\n"
                        f"👤 {title}\n\n"
                        f"Venez lui souhaiter la bienvenue :\n"
                        f"{link}"
                    )

        except Exception as e:
            print("Erreur :", e)

        await asyncio.sleep(120)


intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")

bot.loop.create_task(check_forum())

bot.run(TOKEN)
