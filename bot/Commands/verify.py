
""" This module represents the verification command, guides new members through the verification flow """

import asyncio
import os

import nextcord 
from bot.bot import Bot
from dotenv import load_dotenv
from nextcord.ext import commands
from nextcord import ButtonStyle
from nextcord.ui import Button, View


load_dotenv(override = True)


guild_id = int(os.getenv("SERVER_ID"))
verified_role_name = os.getenv("ROLE_NAME")
verification_channel_id = int(os.getenv("VERIFY_CHANNEL_ID"))
mod_channel = int(os.getenv("ADMIN_CHANNEL"))


class Verify(commands.Cog):
    """ This class/cog is for the verification command """

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @nextcord.slash_command(name = "verify", guild_ids = [guild_id], description = "Start Verification")
    async def verify(self, interaction: nextcord.Interaction) -> None:
        """
        This function handles member verification.

        ## Args: 
            - name (str): Command name
            - guild_ids (list): list of guild/server IDs where the command should be used
            - description (str): Command description 
            - role (str): Verified role name
            - verify (callable obj): Button object setup for verification interaction
            - label (str): Button text
            - style (ButtonStyle): Sets button color
            - emoji (Unicode/Codepoints): Adds corresponding emoji to the button
            - disabled (bool): whether the button is active (interactable) or disabled (greyed out)

        Raises: 
            Generic error cause procrastinating on this

        """
        # Verified role to be given
        role = nextcord.utils.get(interaction.guild.roles, name = verified_role_name)

        # Button objects, Refer to documentation for attributes
        verify = Button(label = "Verify", style = ButtonStyle.success, emoji = "\N{White Heavy Check Mark}", disabled = False)

        # Button object callback functions, this handles what happens when the corresponding button is pressed, message is then edited to disable buttons
        # XXXX_callback where "XXXX" is the name of the button object 
        async def verify_callback(interaction: nextcord.Interaction) -> None: 
            try:
                verify.disabled = True
                await interaction.response.edit_message(view = verify_view)
                await interaction.send("just a sec", ephemeral = True)
                await asyncio.sleep(3) # Sleep here fixes the occasional bug where role isn't added
                await interaction.send("you're now verified!", ephemeral = True)
                await asyncio.sleep(3) # Sleep here fixes the occasional bug where role isn't added
                await interaction.user.add_roles(role)

            except:
                await interaction.send("Oops something went wrong, please contact administrator!")

        # Sets the callback attribute of the button object as the callback function above
        verify.callback = verify_callback

        # Button views [currently per message view with a timeout of 30 seconds]
        verify_view = View(timeout = 30)

        # Items [i.e. buttons] added to the view [per message]
        verify_view.add_item(verify)

        # Interaction response message when initiating the verification command, checks if channel is correct 
        score = self.bot.threat_scores.get(interaction.user.id, {}).get("score", 0)
        is_bot = self.bot.threat_scores.get(interaction.user.id, {}).get("is_bot")
        is_spam = self.bot.threat_scores.get(interaction.user.id, {}).get("is_spam")


        try: 
            if interaction.channel_id == verification_channel_id:
                if role not in interaction.user.roles:

                    if score < 20:
                        await interaction.send("By completing verification you are agreeing to the rules!", view = verify_view, ephemeral = True)

                    elif score >= 20 or is_bot is True or is_spam is True:
                        await interaction.send(
                            "Sorry you're account has been flagged as suspicious, a private channel will be created for you with server moderators.", ephemeral = True
                        )

                else:
                    await interaction.send("You're already verified", ephemeral = True)

            else: 
                await interaction.send("This command cannot be used here", ephemeral = True)

        except Exception as e:
            await interaction.send("Oops something went wrong, please contact a mod!", ephemeral = True)
            await self.bot.get_channel(mod_channel).send(
                f"The following error occurred while trying to verify {interaction.user.name}\n{type(e).__name__} - {e}"
            )


# Registers the class/cog with the bot, supports loading/unloading although not implemented currently            
def setup(bot: Bot) -> None:
    bot.add_cog(Verify(bot))