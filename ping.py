import nextcord
from nextcord.ext import commands

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def pong(self, ctx):
        await ctx.send("Pong!")

def setup(bot:commands.Bot):
    bot.add_cog(ping(bot))