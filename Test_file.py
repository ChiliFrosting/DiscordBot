import json 



message= {'metadata': {'message_id': '767a350a-0df5-43b6-a816-ce9d2b5c1e61', 'message_type': 'session_welcome', 'message_timestamp': '2024-11-27T00:54:28.531176162Z'}, 'payload': {'session': {'id': 'AgoQ2o7EaOd7TG-b1sEJ1XN5VRIGY2VsbC1j', 'status': 'connected', 'connected_at': '2024-11-27T00:54:28.52632609Z', 'keepalive_timeout_seconds': 10, 'reconnect_url': None, 'recovery_url': None}}}
jason= json.loads(str(message))

print(jason)