import util

# Passes roles and adds them to the user if they exist and are available.
async def add_roles(message):
    role_str = message.content.removeprefix("/role add")
    roles = util.parse_roles(role_str)

    guild_config = util.load_config(message.guild.id)

    added_str, failed_str, block_str = "", "", ""
    for role in roles:
        role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
        if role_obj != None:

            # Check blacklist mode
            if guild_config["blacklist_mode"]:
                if role_obj.id not in guild_config["blacklist_roles"]:
                    await message.author.add_roles(role_obj)
                    await util.log(f"Giving role {role_obj.name} (id={role_obj.id}) to user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                    added_str += f", {role_obj.name}"
                
                else:
                    block_str += f", {role_obj.name}"

            else:
                if role_obj.id in guild_config["whitelist_roles"]:
                    await message.author.add_roles(role_obj)
                    await util.log(f"Giving role {role_obj.name} (id={role_obj.id}) to user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                    added_str += f", {role_obj.name}"

                else:
                    block_str += f", {role_obj.name}"
        else:
            failed_str += f", {role}"

    # Generate msg string
    str = ""
    if guild_config["blacklist_mode"]:
        if added_str != "":
            str += f"The following roles were added:{added_str.removeprefix(",")}.\n"
        if failed_str != "":
            str += f"The following roles were not found:{failed_str.removeprefix(",")}.\n"
        if block_str != "":
            str += f"The following roles are blacklisted:{block_str.removeprefix(",")}.\n"
    else:
        if added_str != "":
            str += f"The following roles were added:{added_str.removeprefix(",")}.\n"
        if failed_str != "":
            str += f"The following roles were not found:{failed_str.removeprefix(",")}.\n"
        if block_str != "":
            str += f"The following roles are not whitelisted:{block_str.removeprefix(",")}.\n"
    
    await util.pkdelay(message)
    await message.channel.send(str)
    
# Passes roles and removes them from the user if they exist and are available.
async def remove_roles(message):
    role_str = message.content.removeprefix("/role remove")
    roles = util.parse_roles(role_str)

    guild_config = util.load_config(message.guild.id)

    removed_str, failed_str, block_str = "", "", ""
    for role in roles:
        role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
        if role_obj != None:

            # Check blacklist mode
            if guild_config["blacklist_mode"]:
                if role_obj.id not in guild_config["blacklist_roles"]:
                    await message.author.remove_roles(role_obj)
                    await util.log(f"Removing role {role_obj.name} (id={role_obj.id}) from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                    removed_str += f", {role_obj.name}"
                
                else:
                    block_str += f", {role_obj.name}"
            
            else:
                if role_obj.id in guild_config["whitelist_roles"]:
                    await message.author.remove_roles(role_obj)
                    await util.log(f"Removing role {role_obj.name} (id={role_obj.id}) from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                    removed_str += f", {role_obj.name}"
                
                else:
                    block_str += f", {role_obj.name}"
        
        else:
           failed_str += f", {role}"

    # Generate msg string
    str = ""
    if guild_config["blacklist_mode"]:
        if removed_str != "":
            str += f"The following roles were removed:{removed_str.removeprefix(",")}.\n"
        if failed_str != "":
            str += f"The following roles were not found:{failed_str.removeprefix(",")}.\n"
        if block_str != "":
            str += f"The following roles are blacklisted:{block_str.removeprefix(",")}.\n"
    else:
        if removed_str != "":
            str += f"The following roles were removed:{removed_str.removeprefix(",")}.\n"
        if failed_str != "":
            str += f"The following roles were not found:{failed_str.removeprefix(",")}.\n"
        if block_str != "":
            str += f"The following roles are not whitelisted:{block_str.removeprefix(",")}.\n"
    
    await util.pkdelay(message)
    await message.channel.send(str)
