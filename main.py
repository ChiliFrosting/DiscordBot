
""" Main entry point """

import asyncio

import aiohttp
from twitch.websocket.websocket_client import websocket_client_runtime
from twitch.OAuth.validate_token import token_validation_task
from twitch.OAuth.App.app import start_app
from bot.bot import bot_task, process_ws_queue


async def main() -> None:
    async with aiohttp.ClientSession() as session:

        await asyncio.gather(
            bot_task(),
            process_ws_queue(),
            websocket_client_runtime(session),
            token_validation_task(session),
            start_app()
        )


asyncio.run(main())