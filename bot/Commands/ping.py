
import os

from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands


load_dotenv(override=True)


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

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name = "ping", description = "are you there?", guild_ids = [guild_id])
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.send("Pong!")


# Registers the ping class/cog with the bot, supports loading/unloading although not currently implemented
def setup(bot):
    bot.add_cog(Ping(bot))