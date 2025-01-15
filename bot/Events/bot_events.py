
import os 

from dotenv import load_dotenv
from nextcord.ext import commands
import nextcord


load_dotenv(override = True)


bot_status_channel = int(os.getenv("STATUS_CHANNEL"))
presence_activity = os.getenv("PRESENCE_ACTIVITY")
presence_url = os.getenv("PRESENCE_URL")


class bot_Events(commands.Cog):
    """ Class/Cog containing Bot related event listeners """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """ 
        This event listener waits for the bot to connect to the Discord API, then sets rich presence & posts ready messages
        """

        await self.bot.change_presence(activity = nextcord.Streaming(name = presence_activity, url = presence_url))
        print(f"Logged in as {self.bot.user}")
        await self.bot.get_channel(bot_status_channel).send("Bot is ready!\n" f"Logged in as {self.bot.user}")


# Registers the class/cog with the bot, supports loading/unloading although not implemented currently
def setup(bot):
    bot.add_cog(bot_Events(bot))