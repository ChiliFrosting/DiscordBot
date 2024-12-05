import asyncio
from websocket.websocket_client import websocket_client_runtime
from bot import bot_task, process_ws_queue

async def main():
    await asyncio.gather(bot_task(), process_ws_queue(), websocket_client_runtime())


asyncio.run(main())