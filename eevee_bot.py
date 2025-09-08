import discord
import os
import dotenv
import asyncio
import util
import registration
import initialisation
import blacklist
import roles
import help

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
    if message.author == client.user:
        return
    
    if (message.webhook_id): 
        return
    
    if message.content.startswith('Hi Eevee'):
        await util.pkdelay(message)
        await message.channel.send("Eevee!")

    elif message.content.startswith('/role add'):
        await roles.add_roles(message)

    elif message.content.startswith('/role remove'):
        await roles.remove_roles(message)

    elif message.content.startswith('/role help'):
        await help.help(message)

    elif message.content == '/role list':
        await help.list_roles(message)

    elif message.content== "/role blacklist mode blacklist" or message.content == "/role blacklist -b":
        if util.is_registered(message):
            await blacklist.blacklist_mode(message, True)
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")
    
    elif message.content == "/role blacklist mode whitelist" or message.content == "/role blacklist -w":
        if util.is_registered(message):
            await blacklist.blacklist_mode(message, False)
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content.startswith('/role blacklist add'):
        if util.is_registered(message):
            await blacklist.blacklist_add(message)
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")
    
    elif message.content.startswith('/role blacklist remove'):
        if util.is_registered(message):
            await blacklist.blacklist_remove(message)
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content.startswith('/role whitelist add'):
        if util.is_registered(message):
            await blacklist.whitelist_add(message)
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content.startswith('/role whitelist remove'):
        if util.is_registered(message):
            await blacklist.whitelist_remove(message)
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content.startswith('/role register'):
        if message.content == "/role register -force" and message.author.guild_permissions.administrator:
            await registration.force(message)
        
        elif util.is_registered(message):
                await registration.register(message)

        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content.startswith('/role deregister'):
        if util.is_registered(message):
            await registration.deregister(message)

        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content.startswith('/role initialise'):
        await initialisation.initialise(message)

    elif message.content.startswith('/role reinitialise'):
        guild_config_file = f"{util.DIR}/guild_configs/{message.guild.id}.json"
        if os.path.isfile(guild_config_file):
            if util.is_registered(message):
                await initialisation.reinitialise(message)

            else:
                await util.log(f"User {message.author.name} (id={message.author.id}) attempted reinitialision of guild {message.guild.name} with id={message.guild.id} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await util.pkdelay(message)
                await message.channel.send(f"Permission denied")
        else:
            await initialisation.initialise(message)

    elif message.content == '/role pkmode on':
        if util.is_registered(message):
            guild_config = util.load_config(message.guild.id)
            guild_config["PK_mode"] = True
            util.save_config(guild_config, message.guild.id)
            await util.log(f"User {message.author.name} (id={message.author.id}) enabled pk mode in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
            await util.pkdelay(message)
            await message.channel.send(f"Server being set to use pk delay. The bot will wait 1 second before responding to allow pk proxy to send.")
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content == '/role pkmode off':
        if util.is_registered(message):
            guild_config = util.load_config(message.guild.id)
            guild_config["PK_mode"] = False
            util.save_config(guild_config, message.guild.id)
            await util.log(f"User {message.author.name} (id={message.author.id}) disabled pk mode in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
            await message.channel.send(f"Server being set to not use pk delay. The bot will respond immediately. Pk proxied messages may send after the bot responds.")
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content == '/role log set':
        if util.is_registered(message):
            guild_config = util.load_config(message.guild.id)
            guild_config["log_channel"] = message.channel.id
            util.save_config(guild_config, message.guild.id)
            await util.log(f"User {message.author.name} (id={message.author.id}) set log channel in channel #{message.channel.name}", guild = message.guild.id, log_type = "LOG")
            await util.pkdelay(message)
            await message.channel.send(f"Eevee bot set to use this channel as the log channel for this server.")
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")

    elif message.content == '/role log off':
        if util.is_registered(message):
            guild_config = util.load_config(message.guild.id)
            guild_config["log_channel"] = None
            util.save_config(guild_config, message.guild.id)
            await util.log(f"User {message.author.name} (id={message.author.id}) disabled logging in channel #{message.channel.name}", guild = message.guild.id, log_type = "LOG")
            await util.pkdelay(message)
            await message.channel.send(f"Eevee bot will no longer log to this server (bot log file will not effected).")
        
        else:
            await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
            await util.pkdelay(message)
            await message.channel.send(f"Permission denied")
    
    elif message.content.startswith("/role small"):
        if message.content.startswith('/role small set'):
            if util.is_registered(message):
                    guild_config = util.load_config(message.guild.id)
                    role = message.content.removeprefix('/role small set ')
                    role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
                    if role_obj != None:
                        guild_config["small_role"] = role_obj.id
                        util.save_config(guild_config, message.guild.id)
                        await util.log(f"User {message.author.name} (id={message.author.id}) set small roll to {role_obj.name} (id={role_obj.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                        await util.pkdelay(message)
                        await message.channel.send(f"Small role set to {role_obj.name} in this server. Small role will now be available to members.")
                    else:
                        await util.pkdelay(message)
                        await message.channel.send(f"Role {role} not found.")
                
            else:
                await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await util.pkdelay(message)
                await message.channel.send(f"Permission denied")

        elif message.content.startswith('/role small time'):
            if util.is_registered(message):
                    guild_config = util.load_config(message.guild.id)
                    time = message.content.removeprefix('/role small time ')
                    if time.isnumeric():
                        guild_config["small_time"] = int(time)
                        util.save_config(guild_config, message.guild.id)
                        await util.pkdelay(message)
                        await message.channel.send(f"Small remove timer set to {guild_config["small_time"]} seconds ({guild_config["small_time"]/60} minutes)")
                    else:
                        await util.pkdelay(message)
                        await message.channel.send(f"Please set time in integer seconds")
                
            else:
                await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await util.pkdelay(message)
                await message.channel.send(f"Permission denied")

        elif message.content == '/role small off':
            if util.is_registered(message):
                guild_config = util.load_config(message.guild.id)
                guild_config["small_role"] = None
                util.save_config(guild_config, message.guild.id)
                await util.log(f"User {message.author.name} (id={message.author.id}) disabled smalls in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                await util.pkdelay(message)
                await message.channel.send(f"Small role will no longer be available in this server.")
            
            else:
                await util.log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await util.pkdelay(message)
                await message.channel.send(f"Permission denied")

        elif message.content == '/role small remove':
            guild_config = util.load_config(message.guild.id)
            if guild_config["small_role"] != None:
                role_obj = next((r for r in message.guild.roles if r.id == guild_config["small_role"]), None)
                if role_obj != None:
                    if any(role.id == guild_config["small_role"] for role in message.author.roles):
                        await util.pkdelay(message)
                        
                        ping_str = ""
                        for role in guild_config["registered_roles"]:
                            reg_role_obj = message.guild.get_role(role)
                            ping_str += f" {reg_role_obj.mention}"

                        await message.channel.send(f"You have requested the {role_obj.name} role be removed, it will be removed in {guild_config["small_time"]} seconds ({guild_config["small_time"]/60} minutes) unless it is removed first first. {ping_str}")
                        await util.log(f"Triggered countdown to remove role {role_obj.name} (id={role_obj.id}) from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                        await asyncio.sleep(guild_config["small_time"])
                        await message.author.remove_roles(role_obj)
                        await util.log(f"Removing role {role_obj.name} (id={role_obj.id}) from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                        await message.channel.send(f"{message.author.mention} the small role {role_obj.name} has been removed if it hadn't already.")
                    else:
                        await util.pkdelay(message)
                        await message.channel.send(f"You are not currently small.")
                
                else:
                    await util.pkdelay(message)
                    await message.channel.send(f"The set small role was not available.")
            
            else:
                await util.pkdelay(message)
                await message.channel.send(f"Small role not set.")
        
        else:
            guild_config = util.load_config(message.guild.id)

            if guild_config["small_role"] != None:
                role_obj = next((r for r in message.guild.roles if r.id == guild_config["small_role"]), None)
                if role_obj != None:
                    await message.author.add_roles(role_obj)
                    await util.log(f"Giving role {role_obj.name} (id={role_obj.id}) to user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                    await util.pkdelay(message)
                    await message.channel.send(f"You have been given the {role_obj.name} role.")

                else:
                    await util.pkdelay(message)
                    await message.channel.send(f"The set small role was not available.")
            
            else:
                await util.pkdelay(message)
                await message.channel.send(f"Small role not set.")



client.run(TOKEN)
