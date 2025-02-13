
""" This module contains all events relevant to guild/server members"""

import asyncio
import os
from datetime import date

from dotenv import load_dotenv
import nextcord
from nextcord.ext import commands


load_dotenv(override = True)


mod_channel = int(os.getenv("ADMIN_CHANNEL"))
mod_role_name = os.getenv("ADMIN_ROLE_NAME")
verification_channel_url = os.getenv("VERIFY_CHANNEL_URL")
verified_role_name = os.getenv("ROLE_NAME")

class member_Events(commands.Cog):
    """ Class/Cog containing member related event listeners """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.unverified = {}
        self.bot.threat_scores = {}
        self.bot.temp_channels = {}


    async def verification_check(self, member: nextcord.Member) -> None:
        """
        Helper function to check if the member completed verification

        Args:
            member (nextcord.Member): passed as the member that triggered the event
        """

        await asyncio.sleep(30)
        role = nextcord.utils.get(member.guild.roles, name = verified_role_name)

        if member.id in self.unverified:
            del self.unverified[member.id]

            if member.id in self.bot.threat_scores: 
                del self.bot.threat_scores[member.id]

            if member.id in self.bot.temp_channels:
                del self.bot.temp_channels[member.id]

            if role not in member.roles: 
                await member.kick(reason = "Did not verify within grace period")
                await self.bot.get_channel(mod_channel).send(
                    f"Member {member.name} was kicked, did not complete verification within grace period."
                )


    async def threat_score(self, member: nextcord.Member) -> tuple[str, bool, bool]:
        """
        This function assigns a score to the member which determines their ability to initiate 
        the verification flow automatically, require manual review or be kicked immediately

        Score is determined as follows: 
            - Account age (< 7 days) -> 40 points
            - Bot (Discord app) account -> auto-restrict
            - Default avatar -> 20
            - known spammer -> auto-restrict
            - Custom avatar -> -5 points
            - Custom banner -> -5 points
            - HypeSquad membership -> -10 points
            - Verified account -> -10 points


        If member has a score of less than 20 -> auto verify available
        If member has a score of 20 or more -> manual review


        ## Args:
            - member (nextcord.Member): passed as member that triggered the event


        ## Returns:
            tuple: a tuple with:
                - int: member score 
                - str: suggested action 
                - bool: if member is a bot, True = Yes
                - bool: if member is flagged as known spammer by discord, True = Yes
        """

        score = 0
        is_bot = False
        is_spam = False

        account_age = (nextcord.utils.utcnow() - member.created_at).days
        hypesquad_member = nextcord.PublicUserFlags.hypesquad
        spammer = nextcord.PublicUserFlags.known_spammer

        if account_age <= 7:
            score += 40

        if member.bot:
            is_bot = True
        
        if member.default_avatar:
            score += 20

        elif member.avatar:
            score -= 5

        if member.banner:
            score -= 5

        if member.pending is False:
            score -= 10

        if hypesquad_member in member.public_flags:
            score -= 10

        if spammer in member.public_flags:
            is_spam = True

        if score >= 20:
            action = "Manual review"
            return score, action, is_bot, is_spam
        
        elif score < 20: 
            action = "Auto Verify"
            return score, action, is_bot, is_spam


    async def create_temp_channel(self, member: nextcord.Member) -> nextcord.TextChannel:
        """
        This is a helper function to create temporary verification channels 
        for users who are not eligible for Auto verification. 
        Creates a Channel visible only to the member and moderator role.

        ## Args: 
            - member (nextcord.Member): member that triggered the event

        
        ## Returns: 
            - nextcord.TextChannel: the created temporary channel
        """

        mod_role = nextcord.utils.get(member.guild.roles, name = mod_role_name)
        temp_channel_name = f"{member.name}-verification-channel"
        permission_overwrites = {
            member.guild.default_role: nextcord.PermissionOverwrite(view_channel = False),
            member: nextcord.PermissionOverwrite(view_channel = True)
        }

        #mod permissions here
        permission_overwrites[mod_role] = nextcord.PermissionOverwrite(view_channel = True)


        temp_channel = await member.guild.create_text_channel(
            name = temp_channel_name,
            overwrites = permission_overwrites
        )

        self.bot.temp_channels[member.id] = {
            "member name" : member.name, 
            "channel name" : temp_channel_name
        }

        await temp_channel.send(f"Hey, {member.mention} this is your temp verification channel.")

        return temp_channel
    

    async def delete_temp_channel(self, temp_channel: nextcord.TextChannel) -> None:
        """
        Helper function to delete temporary verification channels. 
        
        ## Args:
            - temp_channel (nextcord.TextChannel): Channel to be deleted

        ## Returns:
            - None
        """

        try: 
            await temp_channel.delete()

        except nextcord.Forbidden:
            await self.bot.get_channel(mod_channel).send(f"I don't have permission to delete {temp_channel}")

        except nextcord.NotFound:
            pass

        except:
            pass
        

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member) -> None:
        """
        This event listener waits for a new member to join the guild/server, sends a welcome message 
        in the system channel if set & directs members to the verification flow, a grace period of 
        24 hours is given when a new member joins to complete verification and aquire the verified 
        role, otherwise they're removed.

        This listener requires the member intents [Intents.members] to function properly

        ## Args:
            - member (nextcord.Member): Member that triggered the event (member joining the server/guild in this case)
        """

        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the lab {member.mention} \n"
                                               "Please read the rules and verify your humanity to access the server!\n"
                                               f"Please use ``/verify`` in {verification_channel_url}, make sure to complete verification within 24 hours.\n"
                                               "Glad to see ya!")
            
        else:
            await self.bot.get_channel(mod_channel).send("GUILD SYSTEM CHANNEL NOT SET!\n" f"User: {member.name} has joined the server on {date.today()}")

        self.unverified[member.id] = member.joined_at

        score, action, is_bot, is_spam = await self.threat_score(member)
        self.bot.threat_scores[member.id] = {
            "member name" : member.name,
            "score" : score,
            "is_bot" : is_bot,
            "is_spam" : is_spam,
            "action" : action
        }
        print(self.bot.threat_scores)

        await self.bot.get_channel(mod_channel).send(
            f"User: {member.name} has joined the server on {date.today()}\n"
            f"Scored {score}\n"
            f"is this member a bot(discord app)? {is_bot}\n"
            f"is this account flagged as spam? {is_spam}\n"
            f"Recommended action: {action}"
        )

        if action == "Manual review":
            await self.bot.get_channel(mod_channel).send(
                f"Auto Verification is disabled for {member.name}"
            )
            temp_channel = await self.create_temp_channel(member)

        await self.verification_check(member)
        await self.delete_temp_channel(temp_channel)


# Register the class/cog with the bot, supports loading/unloading although not currently implemented           
def setup(bot: commands.Bot) -> None:
    bot.add_cog(member_Events(bot))