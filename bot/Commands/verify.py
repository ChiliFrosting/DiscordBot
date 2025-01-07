
from time import sleep
import os

import nextcord 
from nextcord.ext import commands
from nextcord import File, ButtonStyle
from nextcord.ui import Button, View
from dotenv import load_dotenv


load_dotenv(override= True)

guild_id = 849857597658103848
verified_role_name= os.getenv("ROLE_NAME")
verification_channel_id= 1294760925617717373
mod_channel= 1294760925617717373

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name= "verify", guild_ids= [guild_id], description= "Start Verification")
    async def verify(self, interaction: nextcord.Interaction):
        
        #verified role
        role = nextcord.utils.get(interaction.guild.roles, name= verified_role_name)

        #Button objects, Refer to documentation for attributes
        verify = Button(label= "Verify", style= ButtonStyle.success, emoji= "\N{White Heavy Check Mark}", disabled= False)

        #Button object callback functions, this handles what happens when the corresponding button is pressed, message is then edited to disable buttons
        #XXXX_callback where "XXXX" is the name of the button object 
        async def verify_callback(interaction): 
            try:
                verify.disabled = True
                await interaction.response.edit_message(view= verify_view)
                await interaction.send("just a sec")
                sleep(3)
                await interaction.send("you're now verified!")
                sleep(3)
                await interaction.user.add_roles(role)
            except:
                await interaction.send("Oops something went wrong, please contact administrator!")

        #sets the callback attribute of the button object as the callback function above
        verify.callback = verify_callback

        #UI views [currently per message view with a timeout of 30 seconds]
        verify_view= View(timeout= 30)

        #Items [i.e. buttons] added to the view [per message currently] 
        verify_view.add_item(verify)

        #interaction response message when initiating the verification command, checks if channel is correct 
        try:
            if interaction.channel_id == verification_channel_id:
                if role not in interaction.user.roles:
                    await interaction.send("By completing verification you are agreeing to the rules!", view= verify_view)
                else:
                    await interaction.send("You're already verified", ephemeral= True)
            else:
                await interaction.send("Command cannot be used here!", ephemeral= True)
        except:
            await interaction.send("Oops something went wrong, please contact administrator!")
            self.bot.get_channel(mod_channel).send(f"something went wrong when verifying user: {interaction.user.global_name} aka {interaction.user.display_name} check terminal logging for details")
            
def setup(bot):
    bot.add_cog(Verify(bot))