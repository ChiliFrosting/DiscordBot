
import asyncio
import json
import os
from datetime import datetime, timezone

import aiohttp
from dotenv import load_dotenv
from twitch.websocket.websocket_message_queue import ws_message_queue
from twitch.subscriptions.stream import stream_online, stream_info
from twitch.subscriptions.users import user_info
from bot.bot import bot


load_dotenv(override=True)


token= os.getenv("twitch_oauth_token")
client_id= os.getenv("twitch_client_id")
websocket_endpoint= os.getenv("twitch_websocket_server")
subscription_endpoint= os.getenv("twitch_eventsub_subscriptions")
broadcaster_id= os.getenv("broadcaster_id")
broadcaster_login= os.getenv("broadcaster_login")
stream_info_endpoint = os.getenv("stream_info_endpoint")


async def websocket_client_runtime(session):
    await bot.wait_until_ready()
    await asyncio.sleep(9)
    
    websocket_url= websocket_endpoint
    while True: 

        try: 
            print(f"Connecting to websocket session @{websocket_url} . . . .")
            async with session.ws_connect(websocket_url) as ws:
                new_websocket_url= await websocket_client(ws, session)
                if new_websocket_url: 
                    print(f"Reconnecting to websocket session . . . .")
                    #websocket_url= new_websocket_url
                    
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

                        status, sub_type, broadcaster= await stream_online(
                            session = session,
                            url = subscription_endpoint,
                            token = token,
                            client_id = client_id,
                            session_id = session_id,
                            broadcaster_id = broadcaster_id
                            )
                        
                        if "stream.online" in sub_type and "enabled" in status: 
                            ws_message= {
                                "message": "subscription_request",
                                "content" : {
                                    "status" : {status}, "type" : {sub_type}, "broadcaster_login" : {broadcaster_login}
                                    }
                                }
                            
                            await ws_message_queue.put(ws_message)
                            
                        elif "stream.online" in sub_type and "disabled" in status: 
                            print(f"Subscription request for {broadcaster_login} failed, status: {status} & type:{sub_type}\nTime: {datetime.now()}")

                        else: 
                            (f"Unexpected error: Subscription request failed, Time: {datetime.now()}")

                    case "session_keepalive":
                        print("Session keepalive frame received")
                        

                    case "notification":
                        print(f"Stream.Online event notification received from endpoint: {websocket_endpoint}")

                        broadcaster_name, stream_game_name, stream_type, stream_title, stream_start_time, stream_thumbnail = await stream_info(
                            session = session,
                            url = stream_info_endpoint,
                            token = token,
                            client_id = client_id,
                            braodcaster_id = broadcaster_id,
                            )
                        
                        channel_image_url = await user_info(session = session, token = token, client_id = client_id, broadcaster_login = broadcaster_login)

                        ws_message= {
                            "message" : "notification",
                            "content" : {
                                "broadcaster_name" : broadcaster_name,
                                "channel_image_url" : channel_image_url,
                                "type" : sub_type,
                                "stream_game" : stream_game_name,
                                "stream_type" : stream_type,
                                "stream_title" : stream_title,
                                "stream_start_time" : stream_start_time,
                                "stream_thumbnail" : stream_thumbnail
                                }
                            }
                            
                        await ws_message_queue.put(ws_message)

                    case "session_reconnect":
                        reconnect_url= message_dict["payload"]["session"]["reconnect_url"]
                        print(reconnect_url)
                        ws_message= {
                            "message" : "reconnect_request",
                            "content" : {
                                "reconnect_url" : reconnect_url
                                }
                            }
                        
                        await ws_message_queue.put(ws_message)

                    case "revocation":
                        print("authorization for subscription revoked")
                        status= message_dict["payload"]["subscription"]["status"]
                        sub_type= message_dict["payload"]["subscription"]["type"]
                        ws_message= {"message" : "revocation", "content" : {"broadcaster_login" : broadcaster_login, "type" : sub_type, "status" : status}}
                        await ws_message_queue.put(ws_message)

            case aiohttp.WSMsgType.CLOSED:
                print(f"Server closed the connection unexpectedly: Websocket Connection Closed Abnormally - {aiohttp.WSCloseCode.ABNORMAL_CLOSURE}")
                await asyncio.sleep(5)
                return
            
            case aiohttp.WSMsgType.CLOSE:
                print(f"Server closed the connection: Websocket Connection Close OK, close frame received - {aiohttp.WSCloseCode.OK}")
                await asyncio.sleep(5)
                return
            
            case _:
                print("Server closed the connection with no status code")
                return