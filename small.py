from datetime import datetime
import discord
import asyncio
import util

# Sets the small role in the guild config.
async def set_small(message):
    guild_config = util.load_config(message.guild.id)
    role = message.content.removeprefix('/role small set ')
    role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
    if role_obj != None:
        guild_config["small_role"] = role_obj.id
        util.save_config(guild_config, message.guild.id)
        await util.log(f"User {message.author.name} (id={message.author.id}) set small roll to {role_obj.name} (id={role_obj.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Small role set to {role_obj.name} in this server.", value="Small role will now be available to members.")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)
    else:
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Role {role} not found.", value="")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)

# Sets the small timer in the guild config.
async def small_time(message):
    guild_config = util.load_config(message.guild.id)
    time = message.content.removeprefix('/role small time ')
    if time.isnumeric():
        guild_config["small_time"] = int(time)
        util.save_config(guild_config, message.guild.id)
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Small remove timer set to {guild_config["small_time"]} seconds ({guild_config["small_time"]/60} minutes).", value="")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)
    else:
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name="Please set time in integer seconds.", value="")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)

# Turns off the small role in the guild config.
async def small_off(message):
    guild_config = util.load_config(message.guild.id)
    guild_config["small_role"] = None
    util.save_config(guild_config, message.guild.id)
    await util.log(f"User {message.author.name} (id={message.author.id}) disabled smalls in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    await util.pkdelay(message)
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    embed.add_field(name="Small role has been disabled.", value="Small role will no longer be available in this server.")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")
    await message.channel.send(embed = embed)

# Triggers timer to remove the small role from the user and ping registered roles.
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

                embed = discord.Embed(colour = discord.Colour.dark_grey())
                embed.add_field(name=f"You have requested the {role_obj.name} role be removed.", value=f"It will be removed in {guild_config["small_time"]} seconds ({guild_config["small_time"]/60} minutes) unless it is removed first first. {ping_str}")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {util.VERSION}")
                await message.channel.send(embed = embed)

                await util.log(f"Triggered countdown to remove role {role_obj.name} (id={role_obj.id}) from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                await asyncio.sleep(guild_config["small_time"])
                
                await message.author.remove_roles(role_obj)
                await util.log(f"Removing role {role_obj.name} (id={role_obj.id}) from user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                embed = discord.Embed(colour = discord.Colour.dark_grey())
                embed.add_field(name=f"Small role removed.", value=f"{message.author.mention} the small role {role_obj.name} has been removed if it hadn't already.")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {util.VERSION}")
                await message.channel.send(embed = embed)
            else:
                await util.pkdelay(message)
                embed = discord.Embed(colour = discord.Colour.dark_grey())
                embed.add_field(name="You are not currently small.", value="")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {util.VERSION}")
                await message.channel.send(embed = embed)
        
        else:
            await util.pkdelay(message)
            embed = discord.Embed(colour = discord.Colour.dark_grey())
            embed.add_field(name="The set small role was not available.", value="")
            embed.timestamp = datetime.now()
            embed.set_footer(text=f"Eevee bot {util.VERSION}")
            await message.channel.send(embed = embed)
    
    else:
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name="Small role not set.", value="")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)

# Adds the small role to the user.
async def small(message):
    guild_config = util.load_config(message.guild.id)
    if guild_config["small_role"] != None:
        role_obj = next((r for r in message.guild.roles if r.id == guild_config["small_role"]), None)
        if role_obj != None:
            await message.author.add_roles(role_obj)
            await util.log(f"Giving role {role_obj.name} (id={role_obj.id}) to user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
            await util.pkdelay(message)
            embed = discord.Embed(colour = discord.Colour.dark_grey())
            embed.add_field(name="You have been given the {role_obj.name} role.", value="Use \"/role small remove\" to remove it.")
            embed.timestamp = datetime.now()
            embed.set_footer(text=f"Eevee bot {util.VERSION}")
            await message.channel.send(embed = embed)

        else:
            await util.pkdelay(message)
            embed = discord.Embed(colour = discord.Colour.dark_grey())
            embed.add_field(name="The set small role was not available.", value="")
            embed.timestamp = datetime.now()
            embed.set_footer(text=f"Eevee bot {util.VERSION}")
            await message.channel.send(embed = embed)
    
    else:
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name="Small role not set.", value="")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)
