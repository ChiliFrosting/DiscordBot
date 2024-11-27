import asyncio
from websockets.asyncio.client import connect
from dotenv import load_dotenv
import os 
import json

load_dotenv(override=True)

websocket_endpoint= os.getenv("twitch_websocket_server")
async def session():
    async with connect(websocket_endpoint) as ws:
        while True:

            message= await ws.recv()
            message_dict= json.loads(message)
            print(type(message_dict))
            message_type= message_dict["metadata"]["message_type"]

            print(message_type)


asyncio.get_event_loop().run_until_complete(session())