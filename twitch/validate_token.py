import requests
import os
from dotenv import load_dotenv


load_dotenv(override= True)


token= os.getenv("twitch_oauth_token")

url = "https://id.twitch.tv/oauth2/validate"
headers = {"Authorization": f"Bearer {token}"}



validate_token = requests.get(url=url, headers=headers)
response = validate_token.json()
print(response)