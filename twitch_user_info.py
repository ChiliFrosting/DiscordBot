import requests



url= "https://api.twitch.tv/helix/users"
headers= {"Authorization": "Bearer aex1wikx56fhnh837dv7q4b8od6shj",
             "Client-Id": "gnltd0pal01dzp6uxogo36s83v4ygm"}
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