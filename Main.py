#libraries & needed dependencies 
import nextcord
from nextcord.ext import commands
from nextcord import File, ButtonStyle
from nextcord.ui import Button, View
from datetime import date
from time import sleep
import os
from dotenv import load_dotenv

#load env variables
load_dotenv(override= True)

#Bot Token
token = os.getenv("BOT_TOKEN")

#Bot intents 
intents = nextcord.Intents.all()
intents.members = True

#Short hand for bot object
bot = commands.Bot(intents = intents)

#Relevant Guild/Server/Channel IDs
guild_id = 849857597658103848
verification_channel_name = os.getenv("VERIFY_CHANNEL_NAME")
verification_channel_id = 1294760925617717373
verification_channel_url = os.getenv("VERIFY_CHANNEL_URL")
mod_channel = 1294760925617717373
bot_status_channel = 1294760925617717373

#Bot handled roles
verified_role_id = os.getenv("ROLE_ID")
verified_role_name = os.getenv("ROLE_NAME")
mod_role_id = os.getenv("ADMIN_ROLE_ID")
mod_role_name = os.getenv("ADMIN_ROLE_NAME")

#loading extensions
try:
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"loaded command: {filename[:-3]}")

    for filename in os.listdir("./Events"):
        if filename.endswith(".py"):
            bot.load_extension(f"Events.{filename[:-3]}")
            print(f"loaded event: {filename[:-3]}")
except: 
    print("Extensions not loaded")


#Initialization, status messages & presence
#@bot.event
#async def on_ready():
#    await bot.change_presence(activity= nextcord.Streaming(name= "from the Twilight zone", url= "https://www.twitch.tv/channel_name"))
#    print(f"Logged in as {bot.user}") 
#    await bot.get_channel(bot_status_channel).send("Bot is ready!\n" f"Logged in as {bot.user}") 
#    if modules == True: 
#        await bot.get_channel(bot_status_channel).send("Modules Loaded!")
#    elif modules == False:
#        await bot.get_channel(bot_status_channel).send("No Modules Loaded!")

#Member joining server event, sends welcome message in system channel (if set) & notify moderators
#@bot.event
#async def on_member_join(member):
#    await bot.get_channel(mod_channel).send(f"User: {member.name} has joined the server on {date.today()}")
#    if member.guild.system_channel is not None:
#        await member.guild.system_channel.send(f"Welcome to the lab {member.mention}! \n"
#                                               "Please read the rules and verify your humanity to access the server!\n"
#                                               f"Please use ``/verify`` in {verification_channel_url}\n"
#                                               "Glad to see ya!")
#    else: 
#        await bot.get_channel(mod_channel).send("GUILD SYSTEM CHANNEL NOT SET!\n" f"User: {member.name} has joined the server on {date.today()}")

#Slash command for verification
@bot.slash_command(name= "verify", guild_ids= [guild_id], description= "Start Verification")
async def verify(interaction: nextcord.Interaction):
    
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
        bot.get_channel(mod_channel).send(f"something went wrong when verifying user: {interaction.user.global_name} aka {interaction.user.display_name} check terminal logging for details")
        
@bot.slash_command(name= "delmsgs", guild_ids= [guild_id], description= "Delete all messages in the channel")
async def delmsgs(interaction: nextcord.Interaction):
    
    #verifies user has moderator role, sets command channel to current channel
    role = nextcord.utils.get(interaction.guild.roles, name= mod_role_name)
    channel = bot.get_channel(interaction.channel_id)

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
            await bot.get_channel(mod_channel).send(f"Channel: {channel} purged on {date.today()}")
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

    #checks if user has moderator role, otherwise it tattletales
    try:
        if role in interaction.user.roles:
            await interaction.send(f"**HALT** :raised_back_of_hand: are you sure you want to delete **ALL** messages in this channel?", view= delmsgs_view, ephemeral= True)
        else: 
            await interaction.send("You do not have permission to use this command!", ephemeral= True)
            await bot.get_channel(mod_channel).send(f"Unauthorized use of command by user: {interaction.user.global_name}")
    except:
        await interaction.send("Oops something went wrong, please contact administrator!")

#Bot run command
bot.run(token) 