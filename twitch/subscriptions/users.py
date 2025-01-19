
""" This module contains all the functions related to Twitch API user subscriptions & info """

async def user_info(session, token, client_id, broadcaster_login):

    headers = {
        "Authorization" : f"Bearer {token}",
        "Client-Id" : client_id
    }
    params = {
        "login" : broadcaster_login
    }
    url = "https://api.twitch.tv/helix/users"

    async with session.get(url = url, headers = headers, params = params) as response:
        response_json = await response.json()

        if response_json["data"]:
            channel_image_url = response_json["data"][0]["profile_image_url"]
            
            return channel_image_url
        
        else: 
            return None
