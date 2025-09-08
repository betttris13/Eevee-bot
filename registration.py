import asyncio
import json
import os
import util

async def register(message):
    if message.mentions:
        str = f""
        guild_config = util.load_config(message.guild.id)
        
        for user in message.mentions:
            if user.id not in guild_config['registered_users']:
                guild_config['registered_users'].append(user.id)
                str += f" {user.mention}"
                await util.log(f"User {user.name} (id={user.id}) has been registered by user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "REGISTRATION")

        util.save_config(guild_config, message.guild.id)
        await util.pkdelay(message)
        await message.channel.send(f"Adding {str} to registered users")
    else:
        role_str = message.content.removeprefix("/role register")
        str = await util.add_roles(message, role_str, "registered_roles")
        await util.pkdelay(message)
        await message.channel.send(str)

async def deregister(message):
    if message.mentions:
            str = f""
            guild_config = util.load_config(message.guild.id)
            
            for user in message.mentions:
                if user.id in guild_config['registered_users']:
                    guild_config['registered_users'].remove(user.id)
                    str += f" {user.mention}"
                    await util.log(f"User {user.name} (id={user.id}) has been deregistered by user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "REGISTRATION")

            util.save_config(guild_config, message.guild.id)
            await util.pkdelay(message)
            await message.channel.send(f"Removing {str} to registered users")
    else:
        role_str = message.content.removeprefix("/role deregister")
        str = await util.remove_roles(message, role_str, "registered_roles")
        await util.pkdelay(message)
        await message.channel.send(str)

async def force(message):
    guild_config_file = f"{util.DIR}/guild_configs/{message.guild.id}.json"
    if os.path.isfile(guild_config_file):
        guild_config = util.load_config(message.guild.id)
        
        if message.author.id not in guild_config['registered_users']:
            guild_config['registered_users'].append(message.author.id)
            await util.log(f"User {message.author.name} (id={message.author.id}) has been registered by user {message.author.name} (id={message.author.id}) in channel #{message.channel.name} using admin override", guild = message.guild.id, message = message, log_type = "REGISTRATION")

        util.save_config(guild_config, message.guild.id)

        await util.pkdelay(message)
        await message.channel.send(f"Forcefully adding {message.author.mention} to registered users using admin override")
    
    else:
        await message.channel.send(f"Server not initialised")