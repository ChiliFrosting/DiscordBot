import nextcord
import os
from nextcord.ext import commands
from nextcord import File, ButtonStyle
from nextcord.ui import Button, View
from datetime import date
from dotenv import load_dotenv



load_dotenv(override=True)

guild_id= 849857597658103848
mod_channel= 1294760925617717373
mod_role_name= os.getenv("ADMIN_ROLE_NAME")

class DelMsgs(commands.cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name= "delmsgs", guild_ids= [guild_id], description= "Delete all messages in the channel")
    async def delmsgs(self, interaction: nextcord.Interaction):
        
        #verifies user has moderator role, sets command channel to current channel
        role = nextcord.utils.get(interaction.guild.roles, name= mod_role_name)
        channel = self.bot.get_channel(interaction.channel_id)

        #Yes & no button objects
        delmsgs_yes= Button(label= "Yes", style= ButtonStyle.danger, emoji= "\N{Wastebasket}", disabled= False)
        delmsgs_no= Button(label= "No", style= ButtonStyle.green, emoji= "\N{Cross Mark}", disabled= False)

        #function for yes button object 
        async def delmsgs_yes_callback(interaction):
            try:
                delmsgs_yes.disabled, delmsgs_no.disabled = True, True
                await interaction.response.edit_message(view= delmsgs_view)
                await channel.purge()
                await interaction.send("purge successful", ephemeral = True)
                await self.bot.get_channel(mod_channel).send(f"Channel: {channel} purged on {date.today()}")
            except:
                await interaction.send("Oops something went wrong, please contact administrator!")
        
        #function for no button object
        async def delmsgs_no_callback(interaction):
            try:
                delmsgs_yes.disabled, delmsgs_no.disabled = True, True
                await interaction.response.edit_message(view= delmsgs_view)
                await interaction.send("Purge canceled", ephemeral = True)
            except:
                await interaction.send("Oops something went wrong, please contact administrator!")

        #button object function callbacks
        delmsgs_yes.callback = delmsgs_yes_callback
        delmsgs_no.callback = delmsgs_no_callback

        #button object view for delmsgs command
        delmsgs_view = View(timeout = 30)

        #add button objects to the delmsgs command view
        delmsgs_view.add_item(delmsgs_yes)
        delmsgs_view.add_item(delmsgs_no)

        #checks if user has moderator role, otherwise it tattles
        try:
            if role in interaction.user.roles:
                await interaction.send(f"**HALT** :raised_back_of_hand: are you sure you want to delete **ALL** messages in this channel?", view= delmsgs_view, ephemeral= True)
            else: 
                await interaction.send("You do not have permission to use this command!", ephemeral= True)
                await self.bot.get_channel(mod_channel).send(f"Unauthorized use of command by user: {interaction.user.global_name}")
        except:
            await interaction.send("Oops something went wrong, please contact administrator!")

def setup(bot):
    bot.add_cog(DelMsgs(bot))