
""" Basic routes """

from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/")
async def index(request: web.Request) -> web.FileResponse:
    """ Homepage """
    return web.FileResponse("app/content/index.html")


@routes.get("/ping")
async def ping(request: web.Request) -> web.Response:
    """ Returns latency to Discord servers """
    bot_instance = request.app["bot"]

    ping_value = f"{round(bot_instance.latency*1000)}ms"

    return web.json_response({"ping" : f"{ping_value}"}, status = 200)
