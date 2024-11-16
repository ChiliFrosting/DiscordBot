import requests
import os
from dotenv import load_dotenv

load_dotenv(override= True)


token= os.getenv("twitch_oauth_token")
client_id= os.getenv("twitch_client_id")

url= "https://api.twitch.tv/helix/users"
headers= {"Authorization": f"Bearer {token}",
             "Client-Id": client_id}
params= {"login": "chili_frosting"}


get_user_id= requests.get(url= url, headers=headers, params=params)
data= get_user_id.json()
#print(data)
user_id= data["data"][0]["id"]
print(f"user ID is {user_id}")

url= "https://api.twitch.tv/helix/channels"
params= {"broadcaster_id": user_id}

channel_info= requests.get(url= url, headers= headers, params= params)
data= channel_info.json()

print(data)