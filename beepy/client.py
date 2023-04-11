import discord
import os
from dotenv import load_dotenv

load_dotenv()

print(1)

class Bot(discord.Bot):
    def __init__(self):
        super().__init__(intents = discord.Intents.all())

bot = Bot()

#connect
bot.run(os.getenv("DISCORD_TOKEN"))

def get_bot():
    return bot