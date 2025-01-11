
async def stream_online(session, url, token, client_id, session_id, broadcaster_id):

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


async def stream_info(session, url, token, client_id, user_id):
    headers = {
        "Authorization" : f"Bearer {token}",
        "Client-Id" : f"{client_id}"
    }
    params = {
        "user_id" : user_id
    }

    async with session.get(url = url, headers = headers, params = params) as response:
        response_json = await response.json()

        stream_game_name = response_json["data"][0]["game_name"]
        stream_type = response_json["data"][0]["type"]
        stream_title = response_json["data"][0]["title"]
        stream_start_time = response_json["data"][0]["started_at"]
        stream_thumbnail = response_json["data"][0]["thumbnail_url"]

        if not stream_type == "live":
            return None
        
        return stream_game_name, stream_type, stream_title, stream_start_time, stream_thumbnail