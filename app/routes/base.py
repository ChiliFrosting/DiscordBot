
""" Basic routes """

from aiohttp import web


routes = web.RouteTableDef()


@routes.get("/")
async def index(request: web.Request) -> web.FileResponse:
    """ Homepage """
    return web.FileResponse("app/content/index.html")