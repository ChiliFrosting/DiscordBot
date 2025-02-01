
import os
from datetime import date
from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View


load_dotenv(override=True)


guild_id= int(os.getenv("SERVER_ID"))
mod_channel= int(os.getenv("ADMIN_CHANNEL"))
mod_role_name= os.getenv("ADMIN_ROLE_NAME")


class DelMsgs(commands.Cog):
    """Class/Cog for channel purge command.
    This command clears all messages in a channel (to an extent, may have to use it a couple times cause its buggy)
    Can be used by admins only. Command can be invoked using slash_commands(/).

    Command uses buttons from the nextcord.ButtonStyle module for an interactive response.

    ## Args:
        name (str): Command name 
        guild_ids (list): list of guild/server IDs where the command can be used
        description (str): Command description


    ## Returns:
        None
    """
    
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name = "delmsgs", guild_ids = [guild_id], description = "Delete all messages in the channel")
    async def delmsgs(self, interaction: nextcord.Interaction):
        
        #verifies user has moderator role, sets command channel to current channel
        role = nextcord.utils.get(interaction.guild.roles, name = mod_role_name)
        channel = self.bot.get_channel(interaction.channel_id)

        """
        Yes & no button objects

        Args: 
            label (str, Optional): Text over button
            style (nextcord.ButtonStyle): sets button color, refer to nextcord docs for possible colors
            emoji (Emoji unicode name, Optional): Emoji displayed
            disabled (bool): whether the button can be clicked or not(greyed out)

        """
        
        delmsgs_yes = Button(label = "Yes", style = ButtonStyle.danger, emoji = "\N{Wastebasket}", disabled = False)
        delmsgs_no = Button(labe = "No", style = ButtonStyle.green, emoji = "\N{Cross Mark}", disabled = False)


        """
        The following two functions edit the Yes & No buttons after interacting with it or a timeout.
        The functions take "interaction" instance as their only argument.
        """ 

        async def delmsgs_yes_callback(interaction):
            try:
                delmsgs_yes.disabled, delmsgs_no.disabled = True, True
                await interaction.response.edit_message(view = delmsgs_view)
                await channel.purge()
                await interaction.send("purge successful", ephemeral = True)
                await self.bot.get_channel(mod_channel).send(f"Channel: {channel} purged on {date.today()}")

            except:
                await interaction.send("Oops something went wrong, please contact administrator!")
        

        # Function for "no" button object
        async def delmsgs_no_callback(interaction):
            try:
                delmsgs_yes.disabled, delmsgs_no.disabled = True, True
                await interaction.response.edit_message(view = delmsgs_view)
                await interaction.send("Purge canceled", ephemeral = True)

            except:
                await interaction.send("Oops something went wrong, please contact administrator!")

        # Don't remember why I did this >_>
        delmsgs_yes.callback = delmsgs_yes_callback
        delmsgs_no.callback = delmsgs_no_callback

        # Button view instance for the interaction
        delmsgs_view = View(timeout = 30)

        # Adds the button objects to the interaction view
        delmsgs_view.add_item(delmsgs_yes)
        delmsgs_view.add_item(delmsgs_no)

        # Checks if user has moderator role, otherwise it tattles
        try:
            if role in interaction.user.roles:
                await interaction.send(f"**HALT** :raised_back_of_hand: are you sure you want to delete **ALL** messages in this channel?", view = delmsgs_view, ephemeral = True)
            
            else:
                await interaction.send("You do not have permission to use this command!", ephemeral = True)
                await self.bot.get_channel(mod_channel).send(f"Unauthorized use of command by user: {interaction.user.global_name}")

        except:
            await interaction.send("Oops something went wrong, please contact administrator!")


# Registers the command Class/Cog with the bot
def setup(bot):
    bot.add_cog(DelMsgs(bot))