import requests
import asyncio
from websocket.websocket_message_queue import ws_token_queue
import os
from dotenv import load_dotenv


load_dotenv(override= True)


token= os.getenv("twitch_oauth_token")

url = "https://id.twitch.tv/oauth2/validate"
headers = {"Authorization": f"Bearer {token}"}

async def token_validation_task():
    while True:
        validate_token = requests.get(url=url, headers=headers)
        response = validate_token.status_code

        if response == 200:
            print("Access Token is valid")
            await asyncio.sleep(3600)

        else: 
            print("Access Token is invalid")
            await asyncio.sleep(3600)