#libraries & needed dependencies 
import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv

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
for filename in os.listdir("./commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"commands.{filename[:-3]}")
        count+= 1
print(f"{count} commands loaded")
    
count= 0
for filename in os.listdir("./Events"):
    if filename.endswith(".py"):
        bot.load_extension(f"Events.{filename[:-3]}")
        count+= 1
print(f"{count} event modules loaded")


#Bot run command
bot.run(token) 