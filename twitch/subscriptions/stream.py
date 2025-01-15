
""" This module contains all the functions related to Twitch API stream subscriptions """

async def stream_online(session, url, token, client_id, session_id, broadcaster_id):
    """
    This function sends a stream.online subscription request through the eventsub API
    for the broadcaster ID provided to it.

    The request is send using HTTP POST via the Aiohtto client session "session"

    Args:
        session (client.session): Aiohttp client.session(), this is passed from the main entry point
        url (str): Eventsub API subscriptions endpoint
        token (str): OAuth access token
        client_id (str): Twitch App client ID (provided by Twitch in the dev dashboard)
        session_id (str): Websocket session ID provided by the welcome message when the websocket client connects 
        broadcaster_id (str): Broadcaster ID of the channel to be subscribed to

    Returns:
        status (str): Subscription request status
        sub_type (str): Subscription type | None if status is "disabled"
        broadcaster (str): Broadcaster ID | None if status is "disabled"
    """

    headers= {
        "Authorization" : f"Bearer {token}",
        "Client-Id" : client_id,
        "Content-Type" : "application/json"
    }

    data= {
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

    async with session.post(url= url, headers= headers, json= data) as response:
        response_json= await response.json()
        status= response_json["data"][0]["status"]

        if "enabled" in status:
            
            sub_type= response_json["data"][0]["type"]
            broadcaster= response_json["data"][0]["condition"]["broadcaster_user_id"]
            print(f"\nSubscription request sucessful!\nSubscription Details:\nType: {sub_type}\nBroadcaster: {broadcaster}")
            return status, sub_type, broadcaster
        else: 
            status, sub_type, broadcaster= "disabled", None, None
            return status, sub_type, broadcaster


async def stream_info(session, url, token, client_id, braodcaster_id):
    """
    This function obtains stream info for the Broadcaster ID provided.

    Args:
        session (Aiohttp Client.session()): Aiohttp client session, passed from the main entry 
        url (str): Twitch Helix API streams endpoint
        token (str): OAuth access token
        client_id (str): Twitch App client ID (provided by Twitch in the dev dashboard)
        broadcaster_id (_type_): Broadcaster ID for whom stream information is requested

    Returns:
        None: if GET request stream_type variable is not "live" (stream is not live)
        stream_game_name (dict | str): streamed game name
        stream_type (dict | str): stream is live: type is live (idk what else it could be, don't want to look it up now)
        stream_title (dict | str): stream title (duh)
        stream_start_time (dict | str): stream start time UTC
        stream_thumbnail (dict | str): stream thumbnail URL, provided by Twitch
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

        broadcaster_user_name = response_json["data"][0]["user_name"]
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
        
        return broadcaster_user_name, stream_game_name, stream_type, stream_title, stream_start_time, stream_thumbnail