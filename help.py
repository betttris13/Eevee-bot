import util

async def help(message):
    help_str = ""
    if util.is_registered(message):
        help_str = "**Available commands:**\n"
        help_str += "/role add role1, role2, ...\nAdds the roles listed after command. Note roles must be comma seperated.\n\n"
        help_str += "/role remove role1, role2, ...\nRemoves the roles listed after command. Note roles must be comma seperated.\n\n"
        help_str += "/role small\nGives the set small role if it is set.\n\n"
        help_str += "/role small remove\nRemoves the set small role after a set time.\n\n"
        help_str += "/role list\nShows a list of available roles.\n\n"
        help_str += "/role help\nShows this message.\n\n"
    
    else:
        help_str = "**Available commands:**\n"
        help_str += "/role add role1, role2, ...\nAdds the roles listed after command. Note roles must be comma seperated.\n\n"
        help_str += "/role remove role1, role2, ...\nRemoves the roles listed after command. Note roles must be comma seperated.\n\n"
        help_str += "/role small\nGives the set small role if it is set.\n\n"
        help_str += "/role small remove\nRemoves the set small role after a set time.\n\n"
        help_str += "/role list\nShows a list of available roles.\n\n"
        help_str += "/role help\nShows this message.\n\n"

    await util.pkdelay(message)
    await message.channel.send(help_str)

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
    await message.channel.send(f"**Available roles:**{available_roles}")