#libraries & needed dependencies 
import nextcord
from nextcord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from websocket.websocket_message_queue import ws_message_queue


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

async def process_queue():
    await bot.wait_until_ready()

    while True: 
        ws_message= ws_message_queue.get()

        if ws_message["message"] == "subscription_request":
            channel_id= 1294760925617717373
            await bot.get_channel(channel_id).send(f"Eventsub subscription request sucessful!\nBroadcaster: {ws_message["content"]["broadcaster"]}\nSubscription Type: {ws_message["content"]["type"]}")

        elif ws_message["message"] == "notification":
            channel_id= 1294760925617717373
            await bot.get_channel(channel_id).send(f"{ws_message["content"]["broadcaster"]} is now streaming!")



#Bot run command
asyncio.run(bot.run(token))