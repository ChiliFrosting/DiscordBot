
""" Settings route """

import traceback

from aiohttp import web


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

    post_config = {
        "broadcaster" : "",
        "announceChannel" : "",
        "verifiedRole" : "",
        "adminRole" : "",
        "adminChannel" : "",
        "statusChannel" : ""
    }

    try: 
        data = await request.json()
        broadcaster = data.get("broadcaster")
        channel_id = int(data.get("announceChannel"))

        post_config["broadcaster"] = broadcaster
        post_config["announceChannel"] = channel_id

        print(post_config)

        return web.json_response({"message" : "Settings updated"}, status = 200)
    
    except Exception as e: 
        traceback.print_exception(e)
        
        return web.json_response({"message" : "Failed to update settings"}, status = 400)
    