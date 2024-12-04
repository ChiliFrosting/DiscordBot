import asyncio
from websocket.websocket_client import websocket_client_runtime
from bot import bot_task, process_queue

async def main():
    await asyncio.gather(bot_task(), websocket_client_runtime(), process_queue())


asyncio.run(main())