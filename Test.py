#Libraries & Dependencies
import nextcord
from nextcord.ext import commands

#Bot intents 
intents = nextcord.Intents.all()
intents.members = True

#Short hand for bot object
bot = commands.Bot(intents = intents)
class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
        guild_id = 849857597658103848

        @bot.slash_command(name= "ping", description= "Test command", guild_ids= [guild_id])
        async def ping(self, interaction : nextcord.Interaction): 
            await interaction.send("Pong!")

def setup(bot):
    bot.add_cog(Test(bot))