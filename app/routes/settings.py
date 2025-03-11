
""" Settings route """

import os
import traceback

import dotenv
from aiohttp import web

env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

routes = web.RouteTableDef()


@routes.get("/settings")
async def twitch_settings(request: web.Request) -> web.FileResponse:
    return web.FileResponse("app/content/settings.html")


@routes.get("/get_channels")
async def get_channels(request: web.Request) -> web.Response:

    bot_instance = request.app["bot"]
    available_channels = []

    for guild in bot_instance.guilds:
        for channel in guild.text_channels:
            available_channels.append({
                "id" : channel.id,
                "name" : f"{guild.name} - #{channel.name}"
            })
    return web.json_response(available_channels)


@routes.get("/get_roles")
async def get_roles(request: web.Request) -> web.Response:

    bot_instance = request.app["bot"]
    guild_roles = []

    for guild in bot_instance.guilds:
        for role in guild.roles:
            guild_roles.append({
                "name": f"{role.name}"
            })
    return web.json_response(guild_roles)


@routes.post("/save_settings")
async def save_settings(request: web.Request) -> web.Response:

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
        
        os.environ["broadcaster_login"] = response.get("broadcaster")
        os.environ["ANNOUNCEMENT_CHANNEL"] = response.get("announceChannel")
        os.environ["ROLE_NAME"] = response.get("verifiedRole")
        os.environ["ADMIN_ROLE_NAME"] = response.get("adminRole")
        os.environ["ADMIN_CHANNEL"] = response.get("adminChannel")
        os.environ["STATUS_CHANNEL"] = response.get("statusChannel")
        
        return web.json_response({"message" : "Settings updated"}, status = 200)
    
    except Exception as e: 
        traceback.print_exception(e)
        return web.json_response({"message" : "Failed to update settings"}, status = 400)
