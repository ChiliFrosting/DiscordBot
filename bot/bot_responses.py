
""" Module to construct bot messages from websocket clients """

import time
from datetime import datetime, timezone

import nextcord


async def twitch_notification(
                broadcaster_name: str,
                profile_image_url: str,
                stream_game: str,
                stream_title: str,
                stream_thumbnail: str,
                channel_url: str,
                bot_name: str,
                bot_icon: str
) -> tuple[nextcord.Embed, nextcord.ui.View]:
    
    """
    Constructor for bot embeds representing Twitch websocket notification
    messages.

    ## Args:
        - Broadcaster_name (str): notifications for this broadcaster/user 
        - Profile_image_url (str): user profile image url
        - Stream_game (str): stream game name
        - Stream_title (str): stream title
        - Stream_thumbnail (str): stream thumbnail url
        - Channel_url (str): broadcaster/user channel url
        - Bot_name (str): name of the discord bot (can be changed to modify embed footer)
        - Bot_icon (str): bot icon url (can be changed to modify icon in embed footer)

    ## Retruns: 
        - nextcord.Embed: A formatted Embed message, an instance of nextcord.Embed class
        - nextcord.ui.View: A view with a button including a url to the channel 
    """

    embed = nextcord.Embed(
        color = nextcord.Color.blurple(),
        title = stream_title,
        type = "rich",
        url = channel_url
    )
    embed.set_author(
        name = f"{broadcaster_name} is now live on Twitch!",
        url = channel_url,
        icon_url = profile_image_url,
    )
    embed.set_image(url = f"{stream_thumbnail}?t={int(time.time())}") # Time is used to bust the cache
    embed.add_field(name = "Game", value = stream_game)
    embed.set_footer(text = bot_name, icon_url = bot_icon)
    embed.timestamp = datetime.now(timezone.utc)


    button = nextcord.ui.Button(
        label = "Click me!",
        style = nextcord.ButtonStyle.link,
        url = channel_url,
        disabled = False
    )

    view = nextcord.ui.View()
    view.add_item(button)


    return embed, view