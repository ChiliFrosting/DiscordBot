import asyncio
import aiohttp
from dotenv import load_dotenv
import os 
import json
from websocket.websocket_message_queue import ws_message_queue
from twitch.subscriptions.stream import stream_online
from datetime import datetime, timezone
from bot.bot import bot


load_dotenv(override=True)


token= os.getenv("twitch_oauth_token")
client_id= os.getenv("twitch_client_id")
websocket_endpoint= os.getenv("twitch_cli_websocket")
subscription_endpoint= os.getenv("twitch_cli_eventsub")
broadcaster_id= os.getenv("broadcaster_id")
broadcaster_login= os.getenv("broadcaster_login")


async def websocket_client_runtime(session):
    await bot.wait_until_ready()
    await asyncio.sleep(5)

    
    websocket_url= websocket_endpoint
    while True: 
        try: 
            print(f"Connecting to websocket session @{websocket_url} . . . .")
            async with session.ws_connect(websocket_url) as ws:
                new_websocket_url= await websocket_client(ws, session)
                if new_websocket_url: 
                    print(f"Reconnecting to websocket session . . . .")
                    websocket_url= new_websocket_url
                    
        except Exception as e: 
            print(f"Websocket error: {type(e).__name__} - {e}")
            print("Retrying in 5 seconds . . . .")
            await asyncio.sleep(5)



async def websocket_client(ws, session):
    while True:
            
        message= await ws.receive()
        match message.type:

            case aiohttp.WSMsgType.TEXT:
                message_dict= json.loads(message.data)
                message_type= message_dict["metadata"]["message_type"]

                match message_type: 

                    case "session_welcome":
                        session_id= message_dict["payload"]["session"]["id"]
                        session_status= message_dict["payload"]["session"]["status"]
                        print(f"\nConnected to websocket session @{websocket_endpoint}, Status: {session_status}")
                        print(f"session ID: {session_id}")


                        status, sub_type, broadcaster= await stream_online(session= session, url=subscription_endpoint, token= token, client_id= client_id, session_id= session_id, broadcaster_id= broadcaster_id)
                        if "stream.online" in sub_type and "enabled" in status: 
                            ws_message= {"message": "subscription_request", "content" : {"status" : {status}, "type" : {sub_type}, "broadcaster_login" : {broadcaster_login}}}
                            await ws_message_queue.put(ws_message)
                            

                        elif "stream.online" in sub_type and "disabled" in status: 
                            print(f"Subscription request for {broadcaster_login} failed, status: {status} & type:{sub_type}\nTime: {datetime.now()}")


                        else: 
                            (f"Unexpected error: Subscription request failed, Time: {datetime.now()}")


                    case "session_keepalive":
                        time= message_dict["metadata"]["message_timestamp"]
                        time_t= datetime.fromisoformat(time.replace("Z", "+00:00"))
                        time_now= datetime.now(timezone.utc)
                        time_diff= time_now - time_t
                        print(time_diff)


                    case "notification":
                        print(f"Event notification received from endpoint: {websocket_endpoint}")
                        ws_message= {"message" : "notification", "content" : {"broadcaster_login" : broadcaster_login, "type" : sub_type}}
                        await ws_message_queue.put(ws_message)


                    case "session_reconnect":
                        reconnect_url= message_dict["payload"]["session"]["reconnect_url"]
                        print(reconnect_url)
                        ws_message= {"message" : "reconnect_request", "content" : {"reconnect_url" : reconnect_url}}
                        await ws_message_queue.put(ws_message)
                        return reconnect_url


                    case "revocation":
                        print("authorization for subscription revoked")
                        status= ["payload"]["subscription"]["status"]
                        sub_type= ["payload"]["subscription"]["type"]
                        ws_message= {"message" : "revocation", "content" : {"broadcaster_login" : broadcaster_login, "type" : sub_type, "status" : status}}
                        await ws_message_queue.put(ws_message)


                    case "close":
                        print("websocket session closed")


            case aiohttp.WSMsgType.CLOSE:
                print(f"server closed the connection with status code: {message.data}")
                await asyncio.sleep(5)
                return