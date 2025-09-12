import discord
from datetime import datetime
import util

# Generates help string and sends it to discord.
async def help(message):
    help_str = ""
    if await util.is_registered(message, do_log = True):
        # help_str = "**Available commands:**\n"
        help_str = "/role add role1, role2, ...\nAdds the roles listed after command. Note roles must be comma separated, commas between \" will be ignored.\n\n"
        help_str += "/role remove role1, role2, ...\nRemoves the roles listed after command. Note roles must be comma separated, commas between \" will be ignored.\n\n"
        help_str += "/role small\nGives the set small role if it is set.\n\n"
        help_str += "/role small remove\nRemoves the set small role after a set time.\n\n"
        help_str += "/role list\nShows a list of available roles.\n\n"
        help_str += "/role help\nShows this message.\n\n"
    
    else:
        # help_str = "**Available commands:**\n"
        help_str = "/role add role1, role2, ...\nAdds the roles listed after command. Note roles must be comma separated, commas between \" will be ignored.\n\n"
        help_str += "/role remove role1, role2, ...\nRemoves the roles listed after command. Note roles must be comma separated, commas between \" will be ignored.\n\n"
        help_str += "/role small\nGives the set small role if it is set.\n\n"
        help_str += "/role small remove\nRemoves the set small role after a set time.\n\n"
        help_str += "/role list\nShows a list of available roles.\n\n"
        help_str += "/role help\nShows this message.\n\n"

    await util.pkdelay(message)
    embed = discord.Embed(title = "**Help documentation:**", colour = discord.Colour.blurple())
    embed.add_field(name="**Available commands:**", value=help_str)
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")
    await message.channel.send(embed=embed)

# Generates list of available roles on the guild and sends it to discord.
async def list_roles(message):
    guild_config = util.load_config(message.guild.id)
    available_roles = ""

    if guild_config["blacklist_mode"]:
        for role in message.guild.roles:
            if role.id == message.guild.id:
                continue
            
            if role.id not in guild_config["blacklist_roles"]:
                available_roles += f"\n{role.name}"
    else:
        for role in message.guild.roles:
            if role.id == message.guild.id:
                continue

            if role.id not in guild_config["whitelist_roles"]:
                continue
            available_roles += f"\n{role.name}"

    await util.pkdelay(message)
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.add_field(name="**Available roles:**", value=available_roles)
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")
    await message.channel.send(embed=embed)