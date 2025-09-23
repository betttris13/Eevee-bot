from datetime import datetime
import discord
import os
import util
import registration
import initialisation
import blacklist
import roles
import help
import small
import emoji

async def role_commands(message):
    # 4 any
    # /role add [role1, "role2", ...]
    # Adds the roles listed after command. Note roles must be comma separated, commas between " will be ignored.
    if message.content.lower().startswith('/role add'):
        await roles.add_roles(message)

    # 6 any
    # /role remove -all
    # Removes the roles listed after command. Note roles must be comma separated, commas between " will be ignored.
    elif message.content.lower() == "/role remove -all":
        await roles.remove_all_roles(message)

    # 5 any
    # /role remove [role1, "role2", ...]
    # Removes the roles listed after command. Note roles must be comma separated, commas between " will be ignored.
    elif message.content.lower().startswith('/role remove'):
        await roles.remove_roles(message)

    # 1 any
    # /role help
    # Shows help message.
    elif message.content.lower().startswith('/role help'):
        await help.role_help(message)
    
    # 3 any
    # /role current
    # Shows a list of current roles
    elif message.content.lower() == '/role current':
        await help.list_roles_user(message)
    
    # 2 any
    # /role list
    # Shows a list of available roles
    elif message.content.lower() == '/role list':
        await help.list_roles(message)

    # 15 admin
    # /role blacklist mode [blacklist/whitelist]
    # Sets blacklist mode to the specified mode.
    elif message.content.lower() == "/role blacklist mode blacklist" or message.content.lower() == "/role blacklist -b":
        if await util.is_registered(message):
            await blacklist.blacklist_mode(message, True)

    # Sets blacklist mode to the specified mode.
    elif message.content.lower() == "/role blacklist mode whitelist" or message.content.lower() == "/role blacklist -w":
        if await util.is_registered(message):
            await blacklist.blacklist_mode(message, False)

    # 13 admin
    # /role blacklist add [role1, "role2", ...]
    # Adds the roles listed after command to the blacklist. Note roles must be comma separated, commas between " will be ignored.
    elif message.content.lower().startswith('/role blacklist add'):
        if await util.is_registered(message):
            await blacklist.blacklist_add(message)

    # 14 admin
    # /role blacklist remove [role1, "role2", ...]
    # Removes the roles listed after command to the blacklist. Note roles must be comma separated, commas between " will be ignored.        
    elif message.content.lower().startswith('/role blacklist remove'):
        if await util.is_registered(message):
            await blacklist.blacklist_remove(message)

    # 11 admin
    # /role whitelist add [role1, "role2", ...]
    # Adds the roles listed after command to the whitelist. Note roles must be comma separated, commas between " will be ignored.
    elif message.content.lower().startswith('/role whitelist add'):
        if await util.is_registered(message):
            await blacklist.whitelist_add(message)

    # 12 admin
    # /role whitelist remove [role1, "role2", ...]
    # Removes the roles listed after command to the whitelist. Note roles must be comma separated, commas between " will be ignored.          
    elif message.content.lower().startswith('/role whitelist remove'):
        if await util.is_registered(message):
            await blacklist.whitelist_remove(message)

    # 9 admin
    # /role register [@user1 @user2 .../role1, "role2", .../-force]
    # Adds the users mentioned or roles listed after command to the list of registered users. Note roles must be comma separated, commas between " will be ignored. -force allows admin to force add themselves to registered user list.
    elif message.content.lower().startswith('/role register'):
        if message.content.lower() == "/role register -force" and message.author.guild_permissions.administrator:
            await registration.force(message)
        
        elif await util.is_registered(message):
            await registration.register(message)

    # 10 admin
    # /role deregister [@user1 @user2 .../role1, "role2", ...]
    # Removes the users mentioned or roles listed after command from the list of registered users. Note roles must be comma separated, commas between " will be ignored.
    elif message.content.lower().startswith('/role deregister'):
        if await util.is_registered(message):
            await registration.deregister(message)

    # 7 admin
    # /role initialise
    # Initialises the server with default configuration and registers the initialising user.
    elif message.content.lower().startswith('/role initialise'):
        await initialisation.initialise(message)

    # 8 admin
    # /role reinitialise
    # Reinitialises the server with default configuration and registers the initialising user. Initialises the server if not initialised.
    elif message.content.lower().startswith('/role reinitialise'):
        
        # Check if guild initialised
        guild_config_file = f"{util.DIR}/guild_configs/{message.guild.id}.json"
        if os.path.isfile(guild_config_file):
            if await util.is_registered(message, False):
                await initialisation.reinitialise(message)

            else:
                await util.log(f"User {message.author.name} (id={message.author.id}) attempted reinitialision of guild {message.guild.name} with id={message.guild.id} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await util.pkdelay(message)
                embed = discord.Embed(colour = discord.Colour.red())
                embed.add_field(name=f"Permission denied", value="You must be registered to use that command.")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {util.VERSION}")
                await message.channel.send(embed=embed)
        
        else:
            await initialisation.initialise(message)

    # 16 admin
    # /role pkmode [on/off]
    # Enables/disables delay before responding to allow pk to proxy msg.
    elif message.content.lower() == '/role pkmode on':
        if await util.is_registered(message):
            await util.pk_on(message)

    # Enables/disables delay before responding to allow pk to proxy msg.
    elif message.content.lower() == '/role pkmode off':
        if await util.is_registered(message):
            await util.pk_off(message)

    # 17 admin
    # /role log set
    # Sets the channel command is sent is as the servers logging channel.
    elif message.content.lower() == '/role log set':
        if await util.is_registered(message):
            await util.log_set(message)

    # 18 admin
    # /role log off
    # Disables bot logging to server.
    elif message.content.lower() == '/role log off':
        if await util.is_registered(message):
            await util.log_off(message)

    elif message.content.lower().startswith("/role small"):

        # 19 admin
        # /role small set [role]
        # Sets the small role on the server.
        if message.content.lower().startswith('/role small set'):
            if await util.is_registered(message):
                await small.set_small(message)
        
        # 20 admin
        # /role small time [time]
        # Sets the small timer value to the provided value in seconds.
        elif message.content.lower().startswith('/role small time'):
            if await util.is_registered(message):
                await small.small_time(message)

        # 21 admin
        # /role small off
        # Disables the small role in the server.
        elif message.content.lower() == '/role small off':
            if await util.is_registered(message):
                await small.small_off(message)

        # 23 any
        # /role small remove
        # Triggers a timer to remove the set small role if it is set and pings the registered roles to remove in the meantime.
        elif message.content.lower() == '/role small remove':
            await small.small_remove(message)
        
        # 22 any
        # /role small
        # Gives the set small role if it is set.
        else:
            await small.small(message)

# Emoji related commands
async def emoji_commands(message):
    # 24 any
    # /emoji help
    # Shows this message.
    if message.content == "/emoji help":
        await help.emoji_help(message)

    # 25 any
    # /emoji get
    # DMs any custom emojis in the message replied to.
    if message.content == "/emoji get":
        await emoji.get_emoji(message)

        
        