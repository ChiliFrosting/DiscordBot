
""" This module contains all events relevant to guild/server members"""

import asyncio
import os
from datetime import date

import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv


load_dotenv(override = True)


mod_channel = int(os.getenv("ADMIN_CHANNEL"))
verification_channel_url = os.getenv("VERIFY_CHANNEL_URL")
verified_role_name = os.getenv("ROLE_NAME")

class member_Events(commands.Cog):
    """ Class/Cog containing member related event listeners """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.unverified = {}

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member) -> None:
        """
        This event listener waits for a new member to join the guild/server, sends a welcome message 
        in the system channel if set & directs members to the verification flow, a grace period of 
        24 hours is given when a new member joins to complete verification and aquire the verified 
        role, otherwise they're removed.

        This listener requires the member intents [Intents.members] to function properly

        Args:
            member (nextcord.Member): The member that triggered the event (member joining the server/guild in this case)
        """

        await self.bot.get_channel(mod_channel).send(f"User: {member.name} has joined the server on {date.today()}")
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the lab {member.mention} \n"
                                               "Please read the rules and verify your humanity to access the server!\n"
                                               f"Please use ``/verify`` in {verification_channel_url}, make sure to complete verification within 24 hours.\n"
                                               "Glad to see ya!")
            
        else:
            await self.bot.get_channel(mod_channel).send("GUILD SYSTEM CHANNEL NOT SET!\n" f"User: {member.name} has joined the server on {date.today()}")

        self.unverified[member.id] = member.joined_at
        print (self.unverified)

        verification_check(member)


        async def verification_check(self, member: nextcord.Member) -> None:
            await asyncio.sleep(86400)

            if member.id in self.unverified:
                del self.unverified[member.id]
                if verified_role_name not in member.roles: 
                    await member.kick(reason = f"{member.name} did not verify within grace period")
            

            

# Register the class/cog with the bot, supports loading/unloading although not currently implemented           
def setup(bot: commands.Bot) -> None:
    bot.add_cog(member_Events(bot))