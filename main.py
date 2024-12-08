import asyncio
import aiohttp
from websocket.websocket_client import websocket_client_runtime
from bot.bot import bot_task, process_ws_queue

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(bot_task(), process_ws_queue(), websocket_client_runtime(session))


asyncio.run(main())