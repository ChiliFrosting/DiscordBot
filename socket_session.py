import asyncio
from websockets.asyncio.client import connect
from dotenv import load_dotenv
import os 
import json
from subscriptions.stream import stream_online

load_dotenv(override=True)


token= os.getenv("twitch_oauth_token")
client_id= os.getenv("twitch_client_id")
websocket_endpoint= os.getenv("twitch_cli_websocket")
subscription_endpoint= os.getenv("twitch_cli_eventsub")


async def session():
    async with connect(websocket_endpoint) as ws:
        while True:
            
            message= await ws.recv()
            message_dict= json.loads(message)
            message_type= message_dict["metadata"]["message_type"]

            if message_type == "session_welcome":

                session_id= message_dict["payload"]["session"]["id"]
                session_status= message_dict["payload"]["session"]["status"]
                print(f"\nConnected to websocket session @{websocket_endpoint}, Status: {session_status}")
                print(f"session ID: {session_id}")

                stream_online(url=subscription_endpoint, token= token, client_id= client_id, session_id= session_id)

            elif message_type == "session_keepalive":
                print(f"Session keep alive received, connected to endpoint: {websocket_endpoint}")

            elif message_type == "notification":
                print(f"Event trigger received from endpoint: {websocket_endpoint}")


asyncio.get_event_loop().run_until_complete(session())