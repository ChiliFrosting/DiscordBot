
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

    print(f"Available Channels: {available_channels}")
    
    return web.json_response(available_channels)


@routes.post("/save_settings")
async def save_settings(request: web.Request) -> web.Response:

    twitch_config = {
        "broadcaster" : "",
        "channel" : ""
    }

    try: 
        data = await request.json()
        broadcaster = data.get("broadcaster")
        channel_id = int(data.get("channel"))

        twitch_config["broadcaster"] = broadcaster
        twitch_config["channel"] = channel_id

        return web.json_response({"message" : "Settings updated"}, status = 200)
    
    except Exception as e: 
        traceback.print_exception(e)
        
        return web.json_response({"message" : "Failed to update settings"}, status = 400)
    