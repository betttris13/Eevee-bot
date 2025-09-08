import asyncio
import json
import os
import util

async def blacklist_add(message):
    role_str = message.content.removeprefix("/role blacklist add")
    str = await util.add_roles(message, role_str, "blacklist_roles")
    await util.pkdelay(message)
    await message.channel.send(str)

async def blacklist_remove(message):
    role_str = message.content.removeprefix("/role blacklist remove")
    str = await util.remove_roles(message, role_str, "blacklist_roles")
    await util.pkdelay(message)
    await message.channel.send(str)

async def whitelist_add(message):
    role_str = message.content.removeprefix("/role whitelist add")
    str = await util.add_roles(message, role_str, "whitelist_roles")
    await util.pkdelay(message)
    await message.channel.send(str)

async def whitelist_remove(message):
    role_str = message.content.removeprefix("/role whitelist remove")
    str = await util.remove_roles(message, role_str, "whitelist_roles")
    await util.pkdelay(message)
    await message.channel.send(str)

async def blacklist_mode(message, blacklist):
    guild_config = util.load_config(message.guild.id)

    await util.log(f"User {message.author.name} (id={message.author.id}) set blacklist mode to {blacklist} in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    if blacklist:
        guild_config["blacklist_mode"] = blacklist
        await util.pkdelay(message)
        await message.channel.send(f"Server being set to use role blacklist. Please note that the blacklist and whitelist need be configured individually and do not share role lists.")
    
    else:
        guild_config["blacklist_mode"] = blacklist
        await util.pkdelay(message)
        await message.channel.send(f"Server being set to use role whitelist. Please note that the blacklist and whitelist need be configured individually and do not share role lists.")

    util.save_config(guild_config, message.guild.id)