import requests



url= "https://id.twitch.tv/oauth2/token"
parameters= {"client_id": "gnltd0pal01dzp6uxogo36s83v4ygm",
         "client_secret": "02t86cqy6e1amyzur8wy9b891qyfu6",
         "grant_type": "client_credentials"}

response= requests.post(url, parameters)

print(response.json())