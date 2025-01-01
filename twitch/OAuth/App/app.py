import asyncio
import os

import dotenv
from aiohttp import web
from bot.bot import bot



# Load the .env file for storing the token
env_file = dotenv.find_dotenv()
dotenv.load_dotenv(env_file)


async def index_handler(request):
    return web.FileResponse("./twitch/OAuth/App/content/index.html")


async def redirect_handler(request):
    return web.FileResponse("./twitch/OAuth/App/content/redirect.html")


async def token_handler(request):
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
    

async def init_app():
    app = web.Application()
    app.router.add_static("/content/", "./twitch/OAuth/App/content")
    app.router.add_get("/", index_handler)
    app.router.add_get("/redirect", redirect_handler)
    app.router.add_post("/token", token_handler)

    return app


async def start_app():
    await bot.wait_until_ready()
    await asyncio.sleep(12)
    app = await init_app()
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


async def shutdown_server():
    """Shuts down the server after a short delay to allow the response to be sent."""
    await asyncio.sleep(1)  # Allow some time for the client to receive the response
    print("Shutting down the server...")
    raise web.GracefulExit  # Trigger the graceful exit of the server