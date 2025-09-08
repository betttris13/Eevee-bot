import asyncio
import util

async def set_small(message):
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

async def small_time(message):
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

async def small_off(message):
    guild_config = util.load_config(message.guild.id)
    guild_config["small_role"] = None
    util.save_config(guild_config, message.guild.id)
    await util.log(f"User {message.author.name} (id={message.author.id}) disabled smalls in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    await util.pkdelay(message)
    await message.channel.send(f"Small role will no longer be available in this server.")

async def small_remove(message):
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

async def small(message):
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
