#libraries & needed dependencies 
import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

#load env variables
load_dotenv(override= True)

#Bot Token
token = os.getenv("BOT_TOKEN")

#Bot intents 
intents = nextcord.Intents.all()
intents.members = True

#Short hand for bot object
bot = commands.Bot(intents = intents)

#loading extensions
count = 0
for filename in os.listdir("./Commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"Commands.{filename[:-3]}")
        count+= 1
print(f"{count} Commands Extensions Loaded")
    
count= 0
for filename in os.listdir("./Events"):
    if filename.endswith(".py"):
        bot.load_extension(f"Events.{filename[:-3]}")
        count+= 1
print(f"{count} Event Extensions Loaded")


#Bot run command
asyncio.run(bot.run(token))