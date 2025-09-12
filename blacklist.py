from datetime import datetime
import discord
import util

# Parses roles and adds them to blacklist in guild config.
async def blacklist_add(message):
    role_str = message.content.removeprefix("/role blacklist add")
    embed = await util.add_roles(message, role_str, "blacklist_roles")
    await util.pkdelay(message)
    await message.channel.send(embed = embed)

# Parses roles and removes them from blacklist in guild config.
async def blacklist_remove(message):
    role_str = message.content.removeprefix("/role blacklist remove")
    embed = await util.remove_roles(message, role_str, "blacklist_roles")
    await util.pkdelay(message)
    await message.channel.send(embed = embed)

# Parses roles and adds them to whitelist in guild config.
async def whitelist_add(message):
    role_str = message.content.removeprefix("/role whitelist add")
    embed = await util.add_roles(message, role_str, "whitelist_roles")
    await util.pkdelay(message)
    await message.channel.send(embed = embed)

# Parses roles and removes them from whitelist in guild config.
async def whitelist_remove(message):
    role_str = message.content.removeprefix("/role whitelist remove")
    embed = await util.remove_roles(message, role_str, "whitelist_roles")
    await util.pkdelay(message)
    await message.channel.send(embed = embed)

# Sets blacklist mode in guild config.
async def blacklist_mode(message, blacklist):
    guild_config = util.load_config(message.guild.id)

    await util.log(f"User {message.author.name} (id={message.author.id}) set blacklist mode to {blacklist} in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    if blacklist:
        guild_config["blacklist_mode"] = blacklist
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Server being set to use role blacklist.", value="Please note that the blacklist and whitelist need be configured individually and do not share role lists.")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)
    
    else:
        guild_config["blacklist_mode"] = blacklist
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Server being set to use role whitelist.", value="Please note that the blacklist and whitelist need be configured individually and do not share role lists.")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)

    util.save_config(guild_config, message.guild.id)