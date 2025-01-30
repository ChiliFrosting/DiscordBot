
"""
Independant testing module. obtain Broadcaster ID from Broadcaster login
Broadcaster login is the broadcaster's user name all lowercase
"""

import asyncio
import os

import aiohttp
from dotenv import load_dotenv


load_dotenv(override= True)


async def user_info():

    token= os.getenv("twitch_oauth_token")
    client_id= os.getenv("twitch_client_id")
    broadcaster_login= os.getenv("broadcaster_login")

    url= "https://api.twitch.tv/helix/users"
    headers= {
        "Authorization": f"Bearer {token}",
        "Client-Id": client_id
        }
    params= {
        "login": broadcaster_login
        }

    async with aiohttp.ClientSession() as session:

        async with session.get(url= url, headers= headers, params= params) as response:

            response_json = await response.json()
            broadcaster_id = response_json["data"][0]["id"]
            print(f"user ID is {broadcaster_id}")

            url= "https://api.twitch.tv/helix/channels"
            params= {
                "broadcaster_id": broadcaster_id
                }
            
        async with session.get(url= url, headers= headers, params= params) as response:
            channel_info= await response.json()

            print(channel_info)


asyncio.run(user_info())