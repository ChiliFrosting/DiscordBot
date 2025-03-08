
""" Main entry point """

import asyncio

import aiohttp
from twitch.websocket.websocket_client import websocket_client_runtime
from twitch.validate_token import twitch_token_validation
from app.app import start_app
from bot.bot import bot_task, process_ws_queue


async def main() -> None:
    async with aiohttp.ClientSession() as session:

        await asyncio.gather(
            bot_task(),
            process_ws_queue(),
            websocket_client_runtime(session),
            twitch_token_validation(session),
            start_app()
        )


asyncio.run(main())