import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)


client_id= os.getenv("twitch_client_id")
client_secret= os.getenv("twitch_client_secret")

url= "https://id.twitch.tv/oauth2/token"
parameters= {"client_id": client_id,
         "client_secret": client_secret,
         "grant_type": "client_credentials"}

response= requests.post(url, parameters)

print(response.json())