
""" This is the web server to use when renewing or generating an OAuth access token """

import asyncio
import os

import dotenv
from aiohttp import web
from bot.bot import bot


# Load the .env file containing the OAuth token
env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)

twitch_config = {
    "broadcaster" : "",
    "channel" : ""
}


async def index_handler(request):
    """ Homepage """

    return web.FileResponse("./twitch/OAuth/App/content/index.html")


async def redirect_handler(request):
    """ Redirect to this page after obtaining access token """

    return web.FileResponse("./twitch/OAuth/App/content/redirect.html")


async def token_handler(request):
    """
    This function handles the POST request from the JavaScript code on the redirect.html file 
    containing the OAuth access token. If the request is OK, the OAuth token in the .env file 
    is overwritten by the new OAuth token.

    Raises: 

        Generic error because I don't like testing error handling
    """

    try: 
        data = await request.json()
        token = data.get("token")
        print("POST request received")

        if token:
            print(f"Received Token: {token}")
            os.environ["twitch_oauth_token"] = token
            dotenv.set_key(env_file, "twitch_oauth_token", token)
            return web.json_response({"message" : "Token Received"}, status = 200)
        
        else: 
            return web.json_response({"message" : "Token not provided"}, status = 400)
           
    except Exception as e: 
        print(f"Error: {e}")
        return web.json_response({"message" : "Bad Request"}, status = 400)
    

async def get_channels(requeset):

    bot_instance = requeset.app["bot"]
    available_channels = []

    for guild in bot_instance.guilds:
        for channel in guild.text_channels:
            available_channels.append({
                "id" : channel.id,
                "name" : f"{guild.name} - #{channel.name}"
            })
    print(f"Available Channels: {available_channels}")
    return web.json_response(available_channels)


async def save_config(request):

    try: 
        data = await request.json()
        broadcaster = data.get("broadcaster")
        channel_id = int(data.get("channel"))

        twitch_config["broadcaster"] = broadcaster
        twitch_config["channel"] = channel_id

        return web.json_response({"message" : "Settings Updated!"}, status = 200)
    
    except Exception as e: 
        return web.json_response({"message" : "Failed to Update Settings!"}, status = 400)


async def twitch_settings_handler(request): 

    return web.FileResponse("./twitch/Oauth/App/content/twitchSettings.html")


async def init_app():
    """ Initialize app instance, add routes, methods & serve HTML files
    in the content directory.

    Returns: 
    
        App instance 
    """

    app = web.Application()
    app.router.add_static("/content/", "./twitch/OAuth/App/content")
    app.router.add_get("/", index_handler)
    app.router.add_get("/redirect", redirect_handler)
    app.router.add_post("/token", token_handler)
    app.router.add_get("/twitchSettings", twitch_settings_handler)
    app.router.add_get("/get_channels", get_channels)
    app.router.add_post("/save_config", save_config)

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