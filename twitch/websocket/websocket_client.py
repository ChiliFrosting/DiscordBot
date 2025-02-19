
""" This module contains all functions related to the websocket client for Twitch"""

import asyncio
import json
import os
from datetime import datetime, timezone

import aiohttp
from bot.async_events import OAuth_valid_event
from bot.bot import bot
from dotenv import load_dotenv
from twitch.websocket.websocket_message_queue import ws_message_queue
from twitch.subscriptions.stream import stream_online, stream_info
from twitch.subscriptions.users import user_info


load_dotenv(override = True)


token = os.getenv("twitch_oauth_token")
client_id = os.getenv("twitch_client_id")
websocket_endpoint = os.getenv("twitch_websocket_server")
subscription_endpoint = os.getenv("twitch_eventsub_subscriptions")
broadcaster_login = os.getenv("broadcaster_login")
stream_info_endpoint = os.getenv("stream_info_endpoint")
status_url = os.getenv("STATUS_URL")


async def twitch_status(session: aiohttp.ClientSession) -> None:
    async with session.get(url = status_url) as response:

        try:
            response_json = await response.json()
            services = response_json.get("components", [])
            non_operational = {}
            critical_services = ["Login", "Video (Broadcasting)", "API"]

            for service in services:
                if service.get("status") != "operational":
                    non_operational[service.get("name", "Unavailable")] = service.get("status", "Unavailable")

            if any(service in non_operational for service in critical_services):
                print("Unable to reach Twitch services")
                await asyncio.sleep(1800)

            else: 
                print(
                    "Twitch services operational.\nLogin -> OK\nAPI -> OK\nVideo (Broadcasting) -> OK\n"
                )
        
        except Exception as e:
            print(
                f"Error occurred while checking status: {type(e).__name__} - {e}\n"
                "Retrying in 30 minutes\n"
            )
            await asyncio.sleep(1800)


async def websocket_client(ws: aiohttp.ClientWebSocketResponse, session: aiohttp.ClientSession) -> None:
    while True:
        
        message = await ws.receive()
        match message.type:

            case aiohttp.WSMsgType.TEXT:
                message_json= json.loads(message.data)
                message_type= message_json["metadata"]["message_type"]

                match message_type: 

                    case "session_welcome":
                        session_id= message_json["payload"]["session"]["id"]
                        session_status= message_json["payload"]["session"]["status"]
                        print(f"\nConnected to websocket session @{websocket_endpoint}, Status: {session_status}")
                        print(f"session ID: {session_id}")

                        broadcaster_id, _ = await user_info(session = session, token = token, client_id = client_id, broadcaster_login = broadcaster_login)

                        status, sub_type, broadcaster = await stream_online(
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
                                    "status" : status, "type" : sub_type, "broadcaster_login" : broadcaster_login
                                    }
                                }
                            
                            await ws_message_queue.put(ws_message)
                            
                        elif "stream.online" in sub_type and "disabled" in status: 
                            print(f"Subscription request for {broadcaster_login} failed, status: {status} & type:{sub_type}\nTime: {datetime.now(timezone.utc)}")

                        else: 
                            (f"Unexpected error: Subscription request failed, Time: {datetime.now(timezone.utc)}")

                    case "session_keepalive":
                        print("Session keepalive frame received")
                        
                        # TODO: add reconnection flow if keepalive frame not received when expected
                        keepalive_timestamp = (message_json["metadata"]["message_timestamp"])[:-2] + "Z"

                        print(f"Keepalive received at: {keepalive_timestamp}")

                        """time_now = datetime.now(timezone.utc)
                        keepalive_timestamp_datetime = datetime.strptime(keepalive_timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                        keepalive_aware = keepalive_timestamp_datetime.replace(tzinfo = timezone.utc)
                        keepalive_delta = time_now - keepalive_aware
                        print(f"last keepalive message @{keepalive_delta.total_seconds()}")"""
                        

                    case "notification":
                        print(f"Stream.Online event notification received from endpoint: {websocket_endpoint}")

                        broadcaster_id, profile_image_url = await user_info(session = session, token = token, client_id = client_id, broadcaster_login = broadcaster_login)

                        broadcaster_name, stream_game, stream_type, stream_title, stream_start_time, stream_thumbnail = await stream_info(
                            session = session,
                            url = stream_info_endpoint,
                            token = token,
                            client_id = client_id,
                            braodcaster_id = broadcaster_id,
                            )

                        ws_message= {
                            "message" : "notification",
                            "content" : {
                                "broadcaster_name" : broadcaster_name,
                                "profile_image_url" : profile_image_url,
                                "type" : sub_type,
                                "stream_game" : stream_game,
                                "stream_type" : stream_type,
                                "stream_title" : stream_title,
                                "stream_start_time" : stream_start_time,
                                "stream_thumbnail" : stream_thumbnail
                                }
                            }
                            
                        await ws_message_queue.put(ws_message)

                    case "session_reconnect":
                        reconnect_url = message_json["payload"]["session"]["reconnect_url"]
                        print(reconnect_url)
                        ws_message = {
                            "message" : "reconnect_request",
                            "content" : {
                                "reconnect_url" : reconnect_url
                                }
                            }
                        
                        await ws_message_queue.put(ws_message)

                    case "revocation":
                        print("authorization for subscription revoked")
                        status = message_json["payload"]["subscription"]["status"]
                        sub_type = message_json["payload"]["subscription"]["type"]

                        ws_message = {
                            "message" : "revocation",
                            "content" : {
                                "broadcaster_login" : broadcaster_login,
                                "type" : sub_type,
                                "status" : status
                            }
                        }
                        
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
         

async def websocket_client_runtime(session: aiohttp.ClientSession) -> None:
    await bot.wait_until_ready()
    
    websocket_url = websocket_endpoint
    while True: 

        try: 
            await OAuth_valid_event.wait()
            await twitch_status(session = session)

            print(f"Connecting to websocket session @{websocket_url} . . . .")
            async with session.ws_connect(websocket_url) as ws:
                new_websocket_url= await websocket_client(ws, session)
                if new_websocket_url: 
                    print(f"Reconnecting to websocket session . . . .")
                    #websocket_url= new_websocket_url
                    
        except Exception as e: 
            print(f"Websocket error: {type(e).__name__} - {e}")
            print("Retrying in 1 minute....")
            await asyncio.sleep(60)