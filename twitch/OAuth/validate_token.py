import asyncio
import os

from dotenv import load_dotenv
from websocket.websocket_message_queue import ws_message_queue
from bot.bot import bot


load_dotenv(override= True)


async def token_validation_task(session):
    """
    According to Twitch API requirements, all apps must validate their OAuth access token 
    hourly, this function does just that. This function runs concurrently with the others
    in the main entry point and shares the event loop.

    invalid token? doesn't do a thing... for now at least
    """
    
    # TODO: flag to stop websocket client from connecting until access token is renewed
    await bot.wait_until_ready()
    await asyncio.sleep(3)

    token= os.getenv("twitch_oauth_token")
    url = "https://id.twitch.tv/oauth2/validate"
    headers = {"Authorization": f"Bearer {token}"}

    while True:
        async with session.get(url= url, headers= headers) as response:
            response_status= response.status
    
            if response_status == 200:
                print("Access Token is valid")
                await asyncio.sleep(3600)

            else: 
                print("Access Token is invalid, new OAuth user access token required")
                ws_message= {
                    "message" : "token_expired"
                    }
                #asyncio event set/unset here
                await ws_message_queue.put(ws_message)
                await asyncio.sleep(3600)
