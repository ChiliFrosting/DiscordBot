
""" Module to construct bot messages from websocket clients """

import asyncio
from datetime import datetime, timezone

import nextcord


async def twitch_notification(broadcaster_name, channel_image_url, stream_game, stream_title, 
                              stream_thumbnail, channel_url, bot_name, bot_icon):
    """
    Constructor for bot embeds representing Twitch websocket notification
    messages
    """
    embed = nextcord.Embed(
        color = nextcord.Color.blurple,
        title = stream_title,
        type = "rich",
        url = channel_url
    )
    embed.set_author(
        name = f"{broadcaster_name} is now live on Twitch!",
        url = channel_url,
        icon_url = channel_image_url,
    )
    embed.set_image(url = stream_thumbnail)
    embed.add_field(name = "Game", value = stream_game)
    embed.set_footer(text = bot_name, icon_url = bot_icon)
    embed.timestamp = datetime.now(timezone.utc)

    return embed