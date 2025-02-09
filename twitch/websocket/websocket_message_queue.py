"""" This module should contain all asyncio queues """

import asyncio


ws_message_queue= asyncio.Queue()
ws_token_queue= asyncio.Queue() # not used