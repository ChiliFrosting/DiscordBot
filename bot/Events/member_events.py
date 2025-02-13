""" This module contains all events relevant to guild/server members"""

import os

from nextcord.ext import commands
from datetime import date
from dotenv import load_dotenv


load_dotenv(override = True)


mod_channel = int(os.getenv("ADMIN_CHANNEL"))
verification_channel_url = os.getenv("VERIFY_CHANNEL_URL")


class member_Events(commands.Cog):
    """ Class/Cog containing member related event listeners """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        """
        This event listener waits for a new member to join the guild/server, sends a welcome message 
        in the system channel if set & directs members to the verification flow

        This listener requires the member intents [Intents.members] to function properly

        Args: 
            member (nextcord.member): The member that triggered the event (member joining the server/guild in this case)
        """

        await self.bot.get_channel(mod_channel).send(f"User: {member.name} has joined the server on {date.today()}")
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the lab {member.mention}! \n"
                                               "Please read the rules and verify your humanity to access the server!\n"
                                               f"Please use ``/verify`` in {verification_channel_url}\n"
                                               "Glad to see ya!")
            
        else:
            await self.bot.get_channel(mod_channel).send("GUILD SYSTEM CHANNEL NOT SET!\n" f"User: {member.name} has joined the server on {date.today()}")


# Register the class/cog with the bot, supports loading/unloading although not currently implemented           
def setup(bot):
    bot.add_cog(member_Events(bot))