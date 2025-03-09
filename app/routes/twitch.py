
""" Twitch related routes """

import os
import traceback

from aiohttp import web 
import dotenv


routes = web.RouteTableDef()

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)


@routes.get("/twitch_oauth_redirect")
async def twitch_oauth(request: web.Request) -> web.FileResponse:
    """ Twitch OAuth redirect -> see twitch dev dashboard """
    return web.FileResponse("app/content/redirect.html")


@routes.post("/twitch_oauth_token")
async def twitch_oauth_token(request:web.Request) -> web.Response:

    try: 
        data = await request.json()
        token = data.get("token")
        print("POST request received")

        if token: 
            print(f"Received Twitch OAuth token: {token}")
            os.environ["twitch_oauth_token"] = token
            dotenv.set_key(env_file, "twitch_oauth_token", token)
            return web.json_response({"message" : "Token Received"}, status = 200)
        
        else: 
            return web.json_response({"message" : "Token not provided"}, status = 400)
        
    except Exception as e: 
        traceback.print_exception(e)

        return web.json_response({"message" : "Error while retrieving token"}, status = 400)

