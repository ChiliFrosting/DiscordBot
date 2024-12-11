import os
from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands



load_dotenv(override=True)


guild_id = int(os.getenv("SERVER_ID"))

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="ping", description="are you there?", guild_ids=[guild_id])
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.send("Pong!")

def setup(bot):
    bot.add_cog(Ping(bot))