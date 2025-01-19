
"""
This module contains all Async events used to start & stop application tasks.
has class "AsyncEvents" & a single predefined global instance of that class "event".

Other instances can be created as needed which will inherit both events within the class.
"""

import asyncio


class AsyncEvents:
    """
    Container for Async events related to application tasks.
    
    has the following events:

        - process_queue_event with asyncio.Event methods
        - OAuth_is_valid_event with asyncio.Event methods
    """

    def __init__(self):

        self.process_queue_event = asyncio.Event()
        """
        Indicates if the Bot is ready to process messages from Async message queue (websocket_message_queue.ws_message) - (set = ready, clear = not ready).
        This event assures that no messages are received before the Bot is ready to process them.
        """

        self.OAuth_is_valid_event = asyncio.Event()
        """
        Indicates if the OAuth access token is valid or not - (set = valid, clear = invalid/expired).
        This event determines whether the websocket client should attempt connection based on the validity of the access token.
        Also determines of the web server should be run allowing for the generation of new access tokens.
        """

