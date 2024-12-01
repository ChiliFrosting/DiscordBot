import requests

def stream_online(url, token, client_id, session_id):

    headers= {
        "Authorization" : f"Bearer {token}",
        "Client-Id" : client_id,
        "Content-Type" : "application/json"
    }

    data= {
        "type" : "stream.online",
        "version" : "1",
        "condition" : {
            "broadcaster_user_id" : "572723176"
        },
        "transport" : {
            "method" : "websocket",
            "session_id" : session_id
        }
    }

    response= requests.post(url= url, headers= headers, json= data)
    post_response= response.json()
    status= post_response["data"][0]["status"]

    if status == "enabled":
        
        sub_type= post_response["data"][0]["type"]
        broadcaster= post_response["data"][0]["condition"]["broadcaster_user_id"]
        print(f"\nSubscription request sucessful!\nSubscription Details:\nType: {sub_type}\nBroadcaster: {broadcaster}")
    return status, sub_type