from datetime import datetime
import os
import discord
import util

# Register users or roles giving them elevated permissions in the server.
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
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Adding {str} to registered users.", value="They will now have privileged access to bot commands.")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)
    else:
        role_str = message.content.removeprefix("/role register")
        embed = await util.add_roles(message, role_str, "registered_roles")
        await util.pkdelay(message)
        await message.channel.send(embed = embed)

# Deregisters users or roles, removing them from having elevated permissions.
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
            embed = discord.Embed(colour = discord.Colour.dark_grey())
            embed.add_field(name=f"Removing {str} from registered users.", value="They will no longer have privileged access to bot commands.")
            embed.timestamp = datetime.now()
            embed.set_footer(text=f"Eevee bot {util.VERSION}")
            await message.channel.send(embed = embed)
    else:
        role_str = message.content.removeprefix("/role deregister")
        embed = await util.remove_roles(message, role_str, "registered_roles")
        await util.pkdelay(message)
        await message.channel.send(embed = embed)

# Force adds a server admin to the registered user list.
async def force(message):
    guild_config_file = f"{util.DIR}/guild_configs/{message.guild.id}.json"
    if os.path.isfile(guild_config_file):
        guild_config = util.load_config(message.guild.id)
        
        if message.author.id not in guild_config['registered_users']:
            guild_config['registered_users'].append(message.author.id)
            await util.log(f"User {message.author.name} (id={message.author.id}) has been registered by user {message.author.name} (id={message.author.id}) in channel #{message.channel.name} using admin override", guild = message.guild.id, message = message, log_type = "REGISTRATION")

        util.save_config(guild_config, message.guild.id)

        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name=f"Forcefully adding {message.author.mention} to registered users using admin override.", value="This user will now have privileged access to bot commands.")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)
    
    else:
        await message.channel.send(embed = util.non_initialised())