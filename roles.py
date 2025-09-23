from datetime import datetime
import discord
import util

# Passes roles and adds them to the user if they exist and are available.
async def add_roles(message):
    role_str = message.content.lower().removeprefix("/role add")
    roles = util.parse_roles(role_str)

    guild_config = util.load_config(message.guild.id)

    added_str, failed_str, block_str, log_str = "", "", "", ""
    for role in roles:
        role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
        if role_obj != None:

            # Check blacklist mode
            if guild_config["blacklist_mode"]:
                if role_obj.id not in guild_config["blacklist_roles"]:
                    await message.author.add_roles(role_obj)
                    added_str += f", {role_obj.name}"
                    log_str += f", {role_obj.name} (id={role_obj.id})"
                
                else:
                    block_str += f", {role_obj.name}"

            else:
                if role_obj.id in guild_config["whitelist_roles"]:
                    await message.author.add_roles(role_obj)
                    added_str += f", {role_obj.name}"
                    log_str += f", {role_obj.name} (id={role_obj.id})"

                else:
                    block_str += f", {role_obj.name}"
        else:
            failed_str += f", {role}"

    # Generate msg string
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    if guild_config["blacklist_mode"]:
        if added_str != "":
            embed.add_field(name=f"The following roles were added:", value=added_str.removeprefix(","))
        if failed_str != "":
            embed.add_field(name=f"The following roles were not found:", value=failed_str.removeprefix(","))
        if block_str != "":
            embed.add_field(name=f"The following roles are blacklisted:", value=block_str.removeprefix(","))
    else:
        if added_str != "":
            embed.add_field(name=f"The following roles were added:", value=added_str.removeprefix(","))
        if failed_str != "":
            embed.add_field(name=f"The following roles were not found:", value=failed_str.removeprefix(","))
        if block_str != "":
            embed.add_field(name=f"The following roles are whitelisted:", value=block_str.removeprefix(","))
    
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")

    if log_str != "":
        await util.log(f"Giving role(s) {log_str.removeprefix(", ")} to user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")

    await util.pkdelay(message)
    await message.channel.send(embed = embed)
    
# Passes roles and removes them from the user if they exist and are available.
async def remove_roles(message):
    role_str = message.content.lower().removeprefix("/role remove")
    roles = util.parse_roles(role_str)

    guild_config = util.load_config(message.guild.id)

    removed_str, failed_str, block_str, log_str = "", "", "", ""
    for role in roles:
        role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
        if role_obj != None:

            # Check blacklist mode
            if guild_config["blacklist_mode"]:
                if role_obj.id not in guild_config["blacklist_roles"]:
                    await message.author.remove_roles(role_obj)
                    removed_str += f", {role_obj.name}"
                    log_str += f", {role_obj.name} (id={role_obj.id})"
                
                else:
                    block_str += f", {role_obj.name}"
            
            else:
                if role_obj.id in guild_config["whitelist_roles"]:
                    await message.author.remove_roles(role_obj)
                    removed_str += f", {role_obj.name}"
                    log_str += f", {role_obj.name} (id={role_obj.id})"
                
                else:
                    block_str += f", {role_obj.name}"
        
        else:
           failed_str += f", {role}"

    # Generate msg string
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    if guild_config["blacklist_mode"]:
        if removed_str != "":
            embed.add_field(name=f"The following roles were removed:", value=removed_str.removeprefix(","))
        if failed_str != "":
            embed.add_field(name=f"The following roles were not found:", value=failed_str.removeprefix(","))
        if block_str != "":
            embed.add_field(name=f"The following roles are blacklisted:", value=block_str.removeprefix(","))
    else:
        if removed_str != "":
            embed.add_field(name=f"The following roles were removed:", value=removed_str.removeprefix(","))
        if failed_str != "":
            embed.add_field(name=f"The following roles were not found:", value=failed_str.removeprefix(","))
        if block_str != "":
            embed.add_field(name=f"The following roles are whitelisted:", value=block_str.removeprefix(","))
    
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")

    if log_str != "":
        await util.log(f"Removing role(s) {log_str.removeprefix(", ")} from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")

    await util.pkdelay(message)
    await message.channel.send(embed = embed)

# Removes all roles from user
async def remove_all_roles(message):
    guild_config = util.load_config(message.guild.id)

    removed_str = ""
    for role_obj in message.author.roles:
        if role_obj != None:
            if role_obj.id == message.guild.id:
                continue

            # Check blacklist mode
            if guild_config["blacklist_mode"]:
                if role_obj.id not in guild_config["blacklist_roles"]:
                    await message.author.remove_roles(role_obj)
                    removed_str += f", {role_obj.name}"
            
            else:
                if role_obj.id in guild_config["whitelist_roles"]:
                    await message.author.remove_roles(role_obj)
                    removed_str += f", {role_obj.name}"

    # Generate msg string
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    if removed_str != "":
        embed.add_field(name=f"The following roles were removed:", value=removed_str.removeprefix(","))
    else:
        embed.add_field(name=f"No roles were removed.", value="If you have roles, they may be black/whitelisted.")
    
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")

    await util.log(f"Removing all roles from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    await util.pkdelay(message)
    await message.channel.send(embed = embed)