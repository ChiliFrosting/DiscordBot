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


bot_ready_event= asyncio.Event()


async def process_ws_queue():
    await bot.wait_until_ready()

    while True: 
        ws_message= await ws_message_queue.get()

        if ws_message["message"] == "subscription_request":
            broadcaster= ws_message["content"]["broadcaster_login"]
            sub_type= ws_message["content"]["type"]
            channel_id= 1294760925617717373

            await bot.get_channel(channel_id).send(f"Eventsub subscription request sucessful!\nBroadcaster: {broadcaster}\nSubscription Type: {sub_type}")
            ws_message_queue.task_done()


        elif ws_message["message"] == "notification":
            channel_id= 1294760925617717373
            await bot.get_channel(channel_id).send(f"{ws_message["content"]["broadcaster_login"]} is now streaming!")
            ws_message_queue.task_done()


#Bot run command
async def bot_task():
    await bot.start(token)