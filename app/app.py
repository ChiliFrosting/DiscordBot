
""" This is the web server to use when renewing or generating an OAuth access token """

import asyncio

from aiohttp import web
from app.routes.base import routes as base_routes
from app.routes.twitch import routes as twitch_routes
from app.routes.settings import routes as settings_routes
from bot.bot import bot


async def init_app():
    """ Initialize app instance, add routes, methods & serve HTML files
    in the content directory.

    Returns: 
    
        App instance 
    """

    app = web.Application()
    app.router.add_static("/content/", "app/content")

    # Routes
    app.add_routes(base_routes)
    app.add_routes(twitch_routes)
    app.add_routes(settings_routes)

    return app


async def start_app():
    """
    Assigned function to run the webserver in the event loop.
    server is run after the Bot is ready. 

    Server is hosted @http://localhost:3000, port 3000 is the required port 
    according to the Twitch API docs 

    a Baserunner instance is used to maintain a single event loop for all the tasks

    Server can be shutdown via keyboard interrupt
    """
    
    await bot.wait_until_ready()
    await asyncio.sleep(5)

    app = await init_app()

    app["bot"] = bot
    
    Baserunner = web.AppRunner(app = app)
    await Baserunner.setup()
    site = web.TCPSite(runner = Baserunner, host = "localhost", port = 3000)
    await site.start()
    print("Server running @ http://localhost:3000, use Ctrl+C to stop the server")

    try: 
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("Keyboard interrupt detected, Stopping the server")
        await Baserunner.cleanup()


# WIP: graceful shutdown of webserver with resource cleanup 
"""async def shutdown_server():
    #Shuts down the server after a short delay to allow the response to be sent.
    await asyncio.sleep(1)  # Allow some time for the client to receive the response
    print("Shutting down the server...")
    raise web.GracefulExit  # Trigger the graceful exit of the server"""