
""" This module contains all the functions related to Twitch API user subscriptions & info """

import aiohttp


async def user_info(
        session: aiohttp.ClientSession,
        token: str,
        client_id: str,
        broadcaster_login: str
) -> tuple[str, str] | None:

    """ 
    Fetch user/broadcaster information.

    ## Args:
    `session` (aiohttp.ClientSession): Aiohttp session instance 
    `token` (str): Twitch OAuth user access token
    `client_id` (str): Twitch app client ID
    `broadcaster_login` (str): Twitch username as in the URL, all lowercase

    ## Returns:
        tuple[[Optional[str], [Optional[str]]: None if broadcaster not found
            - str: Twitch broadcaster ID
            - str: Twitch broadcaster profile image URL
    """

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
            broadcaster_id = response_json["data"][0]["id"]
            profile_image_url = response_json["data"][0]["profile_image_url"]
            
            return broadcaster_id, profile_image_url
        
        else: 
            return None
