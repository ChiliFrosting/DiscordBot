
""" This module contains all the functions related to Twitch API stream subscriptions & info """

async def stream_online(session, url, token, client_id, session_id, broadcaster_id):
    """
    This function sends a stream.online subscription request through the eventsub API
    for the broadcaster ID provided to it.
    
    The request is sent using POST via the Aiohtto client session instance "session"

    ## Args:
    `session` (`aiohttp.ClientSession`): Aiohttp session instance
    `url` (str): Eventsub API subscriptions endpoint
    `token` (str): OAuth access token
    `client_id` (str): Twitch App client ID (provided by Twitch in the dev dashboard)
    `session_id` (str): Websocket session ID provided by the welcome message when connecting 
    `broadcaster_id` (str): Broadcaster ID of the channel to be subscribed to

    ## Returns:
    Tuple[str, Optional[str], Optional[str]]:
        - str: subscriptions status (enabled/disabled)
        - str: subscription type (Refer to Twitch API docs on subscription types) or None 
        - str: broadcaster user ID of the subscription or None 
    """

    headers = {
        "Authorization" : f"Bearer {token}",
        "Client-Id" : client_id,
        "Content-Type" : "application/json"
    }

    data = {
        "type" : "stream.online",
        "version" : "1",
        "condition" : {
            "broadcaster_user_id" : broadcaster_id
        },
        "transport" : {
            "method" : "websocket",
            "session_id" : session_id
        }
    }

    async with session.post(url = url, headers = headers, json = data) as response:
        response_json = await response.json()
        status = response_json["data"][0]["status"]

        if "enabled" in status:
            
            sub_type = response_json["data"][0]["type"]
            broadcaster = response_json["data"][0]["condition"]["broadcaster_user_id"]
            print(f"\nSubscription request sucessful!\nSubscription Details:\nType: {sub_type}\nBroadcaster: {broadcaster}")
            return status, sub_type, broadcaster
        else: 
            status, sub_type, broadcaster= "disabled", None, None
            return status, sub_type, broadcaster


async def stream_info(session, url, token, client_id, braodcaster_id):
    """
    This function obtains stream info for the Broadcaster ID provided.

    ## Args:
    `session` (Aiohttp Client.session()): Aiohttp client session
    `url` (str): Twitch Helix API streams endpoint
    `token` (str): OAuth access token
    `client_id` (str): Twitch App client ID (provided by Twitch in the dev dashboard)
    `broadcaster_id` (str): Broadcaster ID for whom stream information is requested

    ## Returns:
    Tuple[Optional[str], [Optional[str], [Optional[str], [Optional[str], [Optional[str]]:
    None if stream_type is not "live"
        - str: streamed game name
        - str: stream is live (type is live idk what else it could be, too lazy to look it up)
        - str: stream title (duh)
        - str: stream start time UTC
        - str: stream thumbnail URL, provided by Twitch
    """

    headers = {
        "Authorization" : f"Bearer {token}",
        "Client-Id" : f"{client_id}"
    }
    params = {
        "user_id" : braodcaster_id
    }

    async with session.get(url = url, headers = headers, params = params) as response:
        response_json = await response.json()

        if response_json["data"]:

            broadcaster_name = response_json["data"][0]["user_name"]
            stream_game_name = response_json["data"][0]["game_name"]
            stream_type = response_json["data"][0]["type"]
            stream_title = response_json["data"][0]["title"]
            stream_start_time = response_json["data"][0]["started_at"]
            stream_thumbnail = response_json["data"][0]["thumbnail_url"].replace("-{width}x{height}", "")
            #Stream thumbnail url: https://static-cdn.jtvnw.net/previews-ttv/live_user_channelName-{width}x{height}.jpg
            #Above URL takes you to a page that doesn't exist, tried a few resolution combinations but still receive a 404 error
            #for now I'm just removing the "-{width}x{height}" substring and the URL works as intended

            if not stream_type == "live":
                return None
            
            return broadcaster_name, stream_game_name, stream_type, stream_title, stream_start_time, stream_thumbnail
        
        else:
            return None