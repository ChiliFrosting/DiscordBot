import os
import asyncio
import dotenv
from aiohttp import web

# Load the .env file for storing the token
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# Define the OAuth token generation endpoint (from environment)
OAuth_endpoint = os.getenv("token_generation_endpoint")
redirect_url = "http://localhost:3000/callback"


async def OAuth_callback(request):
    """Sends the token capture HTML page to the client."""
    file_path = os.path.join(os.path.dirname(__file__), "token_capture.html")
    return web.FileResponse(file_path)


async def capture_token(request):
    """Captures the token sent from the client (after user consent) and saves it to the .env."""
    try:
        # Get the token from the JSON body of the request
        data = await request.json()
        new_token = data.get("token")

        if not new_token:
            raise ValueError("Token not found in request")

        # Save token to environment variable and .env file
        os.environ["twitch_oauth_token"] = new_token
        dotenv.set_key(dotenv_file, "twitch_oauth_token", new_token)
        print(f"New Access Token: {new_token}")

        # Send success response back to the client
        await shutdown_server()  # Shutdown the server after capturing the token

        return web.json_response({"status": "success", "message": "Token captured successfully"})

    except Exception as e:
        print(f"Error occurred while capturing the token: {type(e)._name_} - {e}")
        return web.json_response({"status": "error", "message": str(e)}, status=500)


async def shutdown_server():
    """Shuts down the server after a short delay to allow the response to be sent."""
    await asyncio.sleep(1)  # Allow some time for the client to receive the response
    print("Shutting down the server...")
    raise web.GracefulExit  # Trigger the graceful exit of the server


async def OAuth_server():
    """Starts the web server and handles access token renewal."""
    app = web.Application()

    # Define routes
    app.router.add_get("/callback", OAuth_callback)
    app.router.add_post("/capture_token", capture_token)

    # Set up the runner to handle the application
    runner = web.AppRunner(app)
    await runner.setup()

    # Start the site on localhost:3000
    site = web.TCPSite(runner, "localhost", 3000)
    await site.start()
    print(f"Webserver running at {redirect_url}")

    try:
        # Keep the server running until the GracefulExit exception is raised
        while True:
            await asyncio.sleep(1)
    except web.GracefulExit:
        print("Webserver shutting down...")
    finally:
        # Clean up the runner after server shutdown
        await runner.cleanup()


async def main():
    """Main function to start the OAuth server."""
    print(f"Go to this URL to renew the access token: {OAuth_endpoint}")
    await OAuth_server()
    print(f"Access token renewed! Access Token: {os.getenv('twitch_oauth_token')}")


asyncio.run(main())