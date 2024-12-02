import asyncio
from websockets.asyncio.client import connect
from dotenv import load_dotenv
import os 
import json
from websocket.websocket_message_queue import ws_message_queue
from twitch.subscriptions.stream import stream_online


load_dotenv(override=True)


token= os.getenv("twitch_oauth_token")
client_id= os.getenv("twitch_client_id")
websocket_endpoint= os.getenv("twitch_cli_websocket")
subscription_endpoint= os.getenv("twitch_cli_eventsub")


async def websocket_client():
    async with connect(websocket_endpoint) as ws:
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

                    status, sub_type, broadcaster= stream_online(url=subscription_endpoint, token= token, client_id= client_id, session_id= session_id)
                    if "stream.online" in sub_type and "enabled" in status: 
                        #send websocket message to queue
                        ws_message= "placeholder"


                case "session_keepalive":
                    print(f"Session keep alive received, connected to endpoint: {websocket_endpoint}")


                case "notification":
                    print(f"Event trigger received from endpoint: {websocket_endpoint}")


                case "session_reconnect":
                    print("reconnect to session here")


                case "revocation":
                    print("authorization for subscription revoked")


                case "close":
                    print("websocket session closed with code(how to check what code?)")


                

asyncio.run(websocket_client())