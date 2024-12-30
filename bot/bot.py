#libraries & needed dependencies 
import os
import asyncio

from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands
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


#channel ids
status_channel= int(os.getenv("STATUS_CHANNEL"))
announcements_channel= int(os.getenv("ANNOUNCEMENT_CHANNEL"))
log_channel= int(os.getenv("LOG_CHANNEL"))
token_url= os.getenv("token_generation_endpoint")

#loading extensions
count = 0
for filename in os.listdir("./bot/Commands"):
    if filename.endswith(".py"):
        bot.load_extension(f"bot.Commands.{filename[:-3]}")
        count+= 1
print(f"{count} Commands Extensions Loaded")
    
count= 0
for filename in os.listdir("./bot/Events"):
    if filename.endswith(".py"):
        bot.load_extension(f"bot.Events.{filename[:-3]}")
        count+= 1
print(f"{count} Event Extensions Loaded")


bot_ready_event= asyncio.Event()


async def process_ws_queue():
    await bot.wait_until_ready()
    await asyncio.sleep(6)
    

    while True: 
        ws_message= await ws_message_queue.get()
        announcements_channel= int(os.getenv("ANNOUNCEMENT_CHANNEL"))
        status_channel= int(os.getenv("STATUS_CHANNEL"))
        log_channel= int(os.getenv("LOG_CHANNEL"))

        if ws_message["message"] == "subscription_request":
            broadcaster= ws_message["content"]["broadcaster_login"]
            sub_type= ws_message["content"]["type"]
            
            await bot.get_channel(status_channel).send(f"Eventsub subscription request sucessful!\nBroadcaster: {broadcaster}\nSubscription Type: {sub_type}")
            ws_message_queue.task_done()


        elif ws_message["message"] == "notification":
            await bot.get_channel(announcements_channel).send(f"{ws_message["content"]["broadcaster_login"]} is now streaming!")
            ws_message_queue.task_done()


        elif ws_message["message"] == "reconnect_request":
            reconnect_url= ws_message["content"]["reconnect_url"]
            await bot.get_channel(log_channel).send(f"Eventsub reconnect request received . . . . reconnecting @{reconnect_url}")
            ws_message_queue.task_done()


        elif ws_message["message"] == "revocation":
            broadcaster_login= ws_message["content"]["broadcaster_login"]
            sub_type= ws_message["content"]["type"]
            status= ws_message["content"]["status"]
            await bot.get_channel(log_channel).send(f"Subscription authorization revoked for {broadcaster_login}\nStatus: {status} - Type: {sub_type}")
            ws_message_queue.task_done()


        elif ws_message["message"] == "token_expired":
            await bot.get_channel(status_channel).send(f"WARNING: Twitch OAuth access token is expired!\nCannot receive notifications until renewed!")
            ws_message_queue.task_done()
            

#Bot run command
async def bot_task():
    await bot.start(token)