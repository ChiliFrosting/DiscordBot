import requests
import json

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

    jheaders= json.dumps(headers)
    jdata= json.dumps(data)

    response= requests.post(url= url, headers= headers, json= data)
    print(response.json())
    return 