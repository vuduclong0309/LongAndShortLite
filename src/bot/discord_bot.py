#MTAzNzA2ODI5MDI1OTk1OTkxOA.GTdn0F.2TEgAoPLDBG-0HleW9hxz7TUlhj-N0s3_BhV6Y

# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = 'MTAzNzA2ODI5MDI1OTk1OTkxOA.GTdn0F.2TEgAoPLDBG-0HleW9hxz7TUlhj-N0s3_BhV6Y'

intents = discord.Intents.default()  
intents.message_content = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    print(message)
    print(message.channel.name)
    if (message.channel.name == "bot-spam"):
        print("msg in channel detected")
        print(message.content)
        if 'out' in message.content.lower():
            print("out detected")

client.run(TOKEN)
