
""" Module to construct bot messages from websocket clients """

from datetime import datetime, timezone

import nextcord


async def twitch_notification(
                broadcaster_name,
                profile_image_url,
                stream_game,
                stream_title,
                stream_thumbnail,
                channel_url,
                bot_name,
                bot_icon
):
    """
    Constructor for bot embeds representing Twitch websocket notification
    messages.

    ## Args:
        - broadcaster_name (str): notifications for this broadcaster/user 
        - profile_image_url (str): user profile image url
        - stream_game (str): stream game name
        - stream_title (str): stream title
        - stream_thumbnail (str): stream thumbnail url
        - channel_url (str): broadcaster/user channel url
        - bot_name (str): name of the discord bot (can be changed to modify embed footer)
        - bot_icon (str): bot icon url (can be changed to modify icon in embed footer)

    ## Retruns: 
        - nextcord.Embed: a formatted Embed message, an instance of nextcord.Embed class
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
    embed.set_image(url = stream_thumbnail)
    embed.add_field(name = "Game", value = stream_game)
    embed.set_footer(text = bot_name, icon_url = bot_icon)
    embed.timestamp = datetime.now(timezone.utc)

    return embed