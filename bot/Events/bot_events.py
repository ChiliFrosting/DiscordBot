
import os 

from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord


bot_status_channel = int(os.getenv("STATUS_CHANNEL"))


class bot_Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity= nextcord.Streaming(name= "from the Twilight zone", url= "https://www.twitch.tv/channel_name"))
        print(f"Logged in as {self.bot.user}")
        await self.bot.get_channel(bot_status_channel).send("Bot is ready!\n" f"Logged in as {self.bot.user}")


def setup(bot):
    bot.add_cog(bot_Events(bot))