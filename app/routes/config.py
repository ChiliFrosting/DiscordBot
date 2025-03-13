
""" Settings route """

import os
import traceback

import dotenv
from aiohttp import web

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

routes = web.RouteTableDef()


@routes.get("/config")
async def config(request: web.Request) -> web.FileResponse:
    """ This is the settings page """
    return web.FileResponse("app/content/config.html")


@routes.post("/save_config")
async def save_config(request: web.Request) -> web.Response:
    """ 
    This route handles POST requests for updating bot configuration.
    POST request is sent/received via the saveConfig.js script.
    The keys expected are as shown in config_keys below, config_keys is a set just for comparison

    The expected POST request body should be:
        JSON = {
        "broadcaster" : "broadcaster login here, this is a string",
        "announceChannel" : "Discord channel where announcements should be sent, this is an integer",
        "verifiedrole" : "Verified role name as written in the server settings, this is a string",
        "adminRole" : "Admin role name as written in the server settings, this is a string",
        "adminChannel" : "Admin channel where member status will be posted, this is an integer",
        "statuschannel" : "Bot status channel where connection/disconnection messages are sent, this is an integer"
        }

    The missing and extra keys are used to validate the request, since all keys are required 
    for the request, however they can be sent and left empty.
    If a parameter is changed, added or removed the request will be ignored and no settings 
    will change. 

    - os.environ -> used to update environment variables dynamically during runtime
    - dotenv.set_key -> used for persistent values saved into the .env file

    """

    config_keys = {
        "broadcaster",
        "announceChannel",
        "verifiedRole",
        "adminRole",
        "adminChannel",
        "statusChannel"
    }

    try:
        response = await request.json()

        missing_keys = config_keys - response.keys()
        extra_keys = response.keys() - config_keys

        if missing_keys or extra_keys:
            print("Missing or unexpected keys")
            return web.json_response({"message" : "Missing or unexpected keys"}, status = 400)
        
        # Set environment variables during runtime
        os.environ["broadcaster_login"] = response.get("broadcaster")
        os.environ["ANNOUNCEMENT_CHANNEL"] = response.get("announceChannel")
        os.environ["ROLE_NAME"] = response.get("verifiedRole")
        os.environ["ADMIN_ROLE_NAME"] = response.get("adminRole")
        os.environ["ADMIN_CHANNEL"] = response.get("adminChannel")
        os.environ["STATUS_CHANNEL"] = response.get("statusChannel")

        # Set persistent environment variables 
        dotenv.set_key(env_file, "broadcaster_login", response.get("broadcaster"))
        dotenv.set_key(env_file, "ANNOUNCEMENT_CHANNEL", response.get("announceChannel"))
        dotenv.set_key(env_file, "ROLE_NAME", response.get("verifiedRole"))
        dotenv.set_key(env_file, "ADMIN_ROLE_NAME", response.get("adminRole"))
        dotenv.set_key(env_file, "ADMIN_CHANNEL", response.get("adminChannel"))
        dotenv.set_key(env_file, "STATUS_CHANNEL", response.get("statusChannel"))
        
        return web.json_response({"message" : "Settings updated"}, status = 200)
    
    except Exception as e: 
        traceback.print_exception(e)
        return web.json_response({"message" : "Failed to update settings"}, status = 400)
