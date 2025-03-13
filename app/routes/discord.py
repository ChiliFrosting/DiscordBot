
""" Discord related routes """

from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/get_channels")
async def get_channels(request: web.Request) -> web.Response:
    """ Backend only route, fetch discord server text channels"""

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
    """ Backend only route, fetch discord server roles """

    bot_instance = request.app["bot"]
    guild_roles = []

    for guild in bot_instance.guilds:
        for role in guild.roles:
            guild_roles.append({
                "name": f"{role.name}"
            })
    return web.json_response(guild_roles)