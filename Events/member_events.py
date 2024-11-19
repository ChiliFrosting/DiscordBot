from nextcord.ext import commands
from datetime import date

mod_channel = 1294760925617717373
VERIFY_CHANNEL_URL= "https://discord.com/channels/849857597658103848/1294760925617717373"

class member_Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.get_channel(mod_channel).send(f"User: {member.name} has joined the server on {date.today()}")
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the lab {member.mention}! \n"
                                               "Please read the rules and verify your humanity to access the server!\n"
                                               f"Please use ``/verify`` in {VERIFY_CHANNEL_URL}\n"
                                               "Glad to see ya!")
        else:
            await self.bot.get_channel(mod_channel).send("GUILD SYSTEM CHANNEL NOT SET!\n" f"User: {member.name} has joined the server on {date.today()}")








def setup(bot):
    bot.add_cog(member_Events(bot))