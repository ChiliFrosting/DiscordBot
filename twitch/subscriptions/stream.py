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