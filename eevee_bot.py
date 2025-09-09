import discord
import os
import dotenv
import util
import registration
import initialisation
import blacklist
import roles
import help
import small

dotenv.load_dotenv()
TOKEN = str(os.getenv("TOKEN"))

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        await util.log(f"Eevee bot connected to {guild.name} (id={guild.id})", guild = guild.id, log_type = "INFO")

@client.event
async def on_message(message):

    # Ignore messages from self
    if message.author == client.user:
        return
    
    # Ignore webhooks
    if message.webhook_id: 
        return
    
    # Cute message to check bot is alive
    if message.content.startswith('Hi Eevee'):
        await util.pkdelay(message)
        await message.channel.send("Eevee!")

    # /role add [role1, role2, ...]
    # Adds the roles listed after command. Note roles must be comma separated.
    elif message.content.startswith('/role add'):
        await roles.add_roles(message)

    # /role remove [role1, role2, ...]
    # Removes the roles listed after command. Note roles must be comma separated.
    elif message.content.startswith('/role remove'):
        await roles.remove_roles(message)

    # /role help
    # Shows help message.
    elif message.content.startswith('/role help'):
        await help.help(message)

    # /role list
    # Shows a list of available roles
    elif message.content == '/role list':
        await help.list_roles(message)

    # /role blacklist mode [blacklist/whitelist]
    # Sets blacklist mode to the specified mode.
    elif message.content== "/role blacklist mode blacklist" or message.content == "/role blacklist -b":
        if await util.is_registered(message):
            await blacklist.blacklist_mode(message, True)

    # Sets blacklist mode to the specified mode.
    elif message.content == "/role blacklist mode whitelist" or message.content == "/role blacklist -w":
        if await util.is_registered(message):
            await blacklist.blacklist_mode(message, False)
    
    # /role blacklist add [role1, role2, ...]
    # Adds the roles listed after command to the blacklist. Note roles must be comma separated.
    elif message.content.startswith('/role blacklist add'):
        if await util.is_registered(message):
            await blacklist.blacklist_add(message)

    # /role blacklist remove [role1, role2, ...]
    # Removes the roles listed after command to the blacklist. Note roles must be comma separated.        
    elif message.content.startswith('/role blacklist remove'):
        if await util.is_registered(message):
            await blacklist.blacklist_remove(message)
    
    # /role whitelist add [role1, role2, ...]
    # Adds the roles listed after command to the whitelist. Note roles must be comma separated.
    elif message.content.startswith('/role whitelist add'):
        if await util.is_registered(message):
            await blacklist.whitelist_add(message)

    # /role whitelist remove [role1, role2, ...]
    # Removes the roles listed after command to the whitelist. Note roles must be comma separated.          
    elif message.content.startswith('/role whitelist remove'):
        if await util.is_registered(message):
            await blacklist.whitelist_remove(message)
    
    # /role register [@user1 @user2 .../role1, role2, .../-force]
    # Adds the users mentioned or roles listed after command to the list of registered users. Note roles must be comma separated. -force allows admin to force add themselves to registered user list.
    elif message.content.startswith('/role register'):
        if message.content == "/role register -force" and message.author.guild_permissions.administrator:
            await registration.force(message)
        
        elif await util.is_registered(message):
            await registration.register(message)

    # /role deregister [@user1 @user2 .../role1, role2, ...]
    # Removes the users mentioned or roles listed after command from the list of registered users. Note roles must be comma separated.
    elif message.content.startswith('/role deregister'):
        if await util.is_registered(message):
            await registration.deregister(message)

    # /role initialise
    # Initialises the server with default configuration and registers the initialising user.
    elif message.content.startswith('/role initialise'):
        await initialisation.initialise(message)

    # /role reinitialise
    # Reinitialises the server with default configuration and registers the initialising user. Initialises the server if not initialised.
    elif message.content.startswith('/role reinitialise'):
        
        # Check if guild initialised
        guild_config_file = f"{util.DIR}/guild_configs/{message.guild.id}.json"
        if os.path.isfile(guild_config_file):
            if await util.is_registered(message, False):
                await initialisation.reinitialise(message)

            else:
                await util.log(f"User {message.author.name} (id={message.author.id}) attempted reinitialision of guild {message.guild.name} with id={message.guild.id} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await util.pkdelay(message)
                await message.channel.send(f"Permission denied")
        
        else:
            await initialisation.initialise(message)

    # /role pkmode [on/off]
    # Enables/disables delay before responding to allow pk to proxy msg.
    elif message.content == '/role pkmode on':
        if await util.is_registered(message):
            await util.pk_on(message)

    # Enables/disables delay before responding to allow pk to proxy msg.
    elif message.content == '/role pkmode off':
        if await util.is_registered(message):
            await util.pk_off(message)
    
    # /role log set
    # Sets the channel command is sent is as the servers logging channel.
    elif message.content == '/role log set':
        if await util.is_registered(message):
            await util.log_set(message)
    
    # /role log off
    # Disables bot logging to server.
    elif message.content == '/role log off':
        if await util.is_registered(message):
            await util.log_off(message)
    
    elif message.content.startswith("/role small"):

        # /role small set [role]
        # Sets the small role on the server.
        if message.content.startswith('/role small set'):
            if await util.is_registered(message):
                await small.set_small(message)
        
        # /role small time [time]
        # Sets the small timer value to the provided value in seconds.
        elif message.content.startswith('/role small time'):
            if await util.is_registered(message):
                await small.small_time(message)

        # /role small off
        # Disables the small role in the server.
        elif message.content == '/role small off':
            if await util.is_registered(message):
                await small.small_off(message)

        # /role small remove
        # Triggers a timer to remove the set small role if it is set and pings the registered roles to remove in the meantime.
        elif message.content == '/role small remove':
            await small.small_remove(message)
        
        # /role small
        # Gives the set small role if it is set.
        else:
            await small.small(message)

@client.event
async def on_error(event, *args, **kwargs):
    if event == 'on_message':
        util.log(f'Unhandled message: {args[0]}', log_type="ERROR")
    else:
        raise

client.run(TOKEN)
