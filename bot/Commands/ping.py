
""" This module represents the ping command, will reply with Pong where ever its invoked """

import asyncio
import datetime
import os
import time

import nextcord
import psutil
from bot.bot import Bot
from dotenv import load_dotenv
from nextcord.ext import commands


load_dotenv(override = True)


guild_id = int(os.getenv("SERVER_ID"))


class Ping(commands.Cog):
    """
    This class/cog is for a ping command, included to check if the bot responds to commands 
    and interactions.

    Args:
        name (str): Command name
        description (str): Command description
        guild_ids (list): List of guild/server IDs where the command should be used
    """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name = "ping", description = "are you there?", guild_ids = [guild_id])
    async def ping(self, interaction: nextcord.Interaction) -> None:
        await interaction.send(
            f"Pong!\n"
            f"Ping: {round(self.bot.latency*1000)}ms\n"
            f"Uptime: {datetime.timedelta(seconds = int(time.time() - self.bot.start_time))}\n"
            f"CPU Usage: {psutil.cpu_percent()}%\n"
            f"Memory Usage: {psutil.virtual_memory().percent}%\n"
            f"Active Tasks: {len(asyncio.all_tasks())}",
            ephemeral = True
        )


# Registers the ping class/cog with the bot, supports loading/unloading although not currently implemented
def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))