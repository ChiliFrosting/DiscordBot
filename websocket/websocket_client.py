import asyncio
from websockets.asyncio.client import connect
from dotenv import load_dotenv
import os 
import json
from websocket.websocket_message_queue import ws_message_queue
from twitch.subscriptions.stream import stream_online
from datetime import datetime
from bot import bot


load_dotenv(override=True)


token= os.getenv("twitch_oauth_token")
client_id= os.getenv("twitch_client_id")
websocket_endpoint= os.getenv("twitch_cli_websocket")
subscription_endpoint= os.getenv("twitch_cli_eventsub")
broadcaster_id= os.getenv("broadcaster_id")
broadcaster_login= os.getenv("broadcaster_login")


async def websocket_client_runtime():
    await bot.wait_until_ready()
    await asyncio.sleep(5)

    
    websocket_url= websocket_endpoint
    while True: 
        try: 
            print(f"Connecting to websocket session @{websocket_url} . . . .")
            async with connect(websocket_url) as ws: 
                new_websocket_url= await websocket_client(ws)
                if new_websocket_url: 
                    print(f"Reconnecting to websocket session . . . .")
                    websocket_url= websocket_url
        except Exception as e: 
            print(f"Websocket error: {type(e).__name__} - {e}")
            print("Retrying in 5 seconds . . . .")
            await asyncio.sleep(5)


async def websocket_client(ws):
    while True:
            
        message= await ws.recv()
        message_dict= json.loads(message)
        message_type= message_dict["metadata"]["message_type"]

        match message_type: 

            case "session_welcome":
                session_id= message_dict["payload"]["session"]["id"]
                session_status= message_dict["payload"]["session"]["status"]
                print(f"\nConnected to websocket session @{websocket_endpoint}, Status: {session_status}")
                print(f"session ID: {session_id}")


                status, sub_type, broadcaster= stream_online(url=subscription_endpoint, token= token, client_id= client_id, session_id= session_id, broadcaster_id= broadcaster_id)
                if "stream.online" in sub_type and "enabled" in status: 
                    ws_message= {"message": "subscription_request", "content" : {"status" : {status}, "type" : {sub_type}, "broadcaster_login" : {broadcaster_login}}}
                    await ws_message_queue.put(ws_message)
                    

                elif "stream.online" in sub_type and "disabled" in status: 
                    print(f"Subscription request for {broadcaster_login} failed, status: {status} & type:{sub_type}\nTime: {datetime.now()}")


                else: 
                    (f"Unexpected error: Subscription request failed, Time: {datetime.now()}")


            case "session_keepalive":
                print(f"Session keep alive received, connected to endpoint: {websocket_endpoint}")


            case "notification":
                print(f"Event notification received from endpoint: {websocket_endpoint}")
                ws_message= {"message" : "notification", "content" : {"broadcaster_login" : broadcaster_login, "type" : sub_type}}
                await ws_message_queue.put(ws_message)


            case "session_reconnect":
                reconnect_url= message_dict["payload"]["session"]["reconnect_url"]
                return reconnect_url


            case "revocation":
                print("authorization for subscription revoked")
                status= ["payload"]["subscription"]["status"]
                sub_type= ["payload"]["subscription"]["type"]
                ws_message= {"message" : "revocation", "content" : {"broadcaster_login" : broadcaster_login, "type" : sub_type, "status" : status}}
                await ws_message_queue.put(ws_message)


            case "close":
                print("websocket session closed")