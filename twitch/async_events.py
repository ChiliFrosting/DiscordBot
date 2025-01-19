
"""
This module contains Asyncio event instances for starting/stopping app tasks.
asyncio.Event() class methods apply.

has the following events:
    - process_queue_event: indicates Bot readiness to receive async queue messages (ready = set, otherwise cleared)
    - OAuth_valid_event: Indicates whether the OAuth token is valid or invalid/expired (valid = set, otherwise cleared)
"""

import asyncio


# Assures Bot not missing any websocket messages
process_queue_event = asyncio.Event()

# Determines whether the websocket client should attemp reconnection
# Determines whether the web server is run to generate a new token
OAuth_valid_event = asyncio.Event()
