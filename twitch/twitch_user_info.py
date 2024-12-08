import asyncio, aiohttp, os
from dotenv import load_dotenv


async def user_info():
    load_dotenv(override= True)

    token= os.getenv("twitch_oauth_token")
    client_id= os.getenv("twitch_client_id")
    broadcaster_login= os.getenv("broadcaster_login")

    url= "https://api.twitch.tv/helix/users"
    headers= {"Authorization": f"Bearer {token}",
                "Client-Id": client_id}
    params= {"login": broadcaster_login}

    async with aiohttp.ClientSession() as session:
        async with session.get(url= url, headers= headers, params= params) as response:
            get_user_id= await response.json()
            print(get_user_id)
            #data= get_user_id.json()
            #print(data)
            user_id= get_user_id["data"][0]["id"]
            print(f"user ID is {user_id}")

            url= "https://api.twitch.tv/helix/channels"
            params= {"broadcaster_id": user_id}
        async with session.get(url= url, headers= headers, params= params) as response:
            channel_info= await response.json()

            print(channel_info)

asyncio.run(user_info())