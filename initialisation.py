import os
import json
import asyncio
import util

async def initialise(message):
    guild_config_file = f"{util.DIR}/guild_configs/{message.guild.id}.json"

    if os.path.isfile(guild_config_file):
        await util.log(f"User {message.author.name} (id={message.author.id}) initialisation of guild {message.guild.name} with id={message.guild.id} in channel #{message.channel.name} failed, guild already initialised", guild = message.guild.id, log_type = "INITIALISATION")
        await util.pkdelay(message)
        await message.channel.send("Server already initialised")
    
    else:
        default_config = {"registered_users": [message.author.id],
                        "registered_roles": [],
                        "whitelist_roles": [],
                        "blacklist_roles": [],
                        "blacklist_mode": False,
                        "small_role": None,
                        "PK_mode": False,
                        "log_channel": None,
                        "small_time": 600,
                        "reset_token": util.id_generator(6)}
        
        with open(guild_config_file, 'x') as f:
            json.dump(default_config, f, indent=4)

        await util.log(f"User {message.author.name} (id={message.author.id}) initialised guild {message.guild.name} with id={message.guild.id} in channel #{message.channel.name}", guild = message.guild.id, log_type = "INITIALISATION")
        await util.log(f"User {message.author.name} (id={message.author.id}) has been registered by user {message.author.name} (id={message.author.id}) as part of initialisation", guild = message.guild.id, log_type = "REGISTRATION")
        await util.pkdelay(message)
        await message.channel.send(f"Server initialised with {message.author.mention} as a registered user")

async def reinitialise(message):
    guild_config = util.load_config(message.guild.id)

    if message.content == f"/role reinitialise {guild_config["reset_token"]}":

        default_config = {"registered_users": [message.author.id],
                        "registered_roles": [],
                        "whitelist_roles": [],
                        "blacklist_roles": [],
                        "blacklist_mode": False,
                        "small_role": None,
                        "PK_mode": False,
                        "log_channel": None,
                        "small_time": 600,
                        "reset_token": util.id_generator(6)}
        
        util.save_config(default_config, message.guild.id)

        await util.log(f"User {message.author.name} (id={message.author.id}) reinitialised guild {message.guild.name} with id={message.guild.id} in channel #{message.channel.name}", guild = message.guild.id, log_type = "INITIALISATION")
        await util.pkdelay(message)
        await message.channel.send(f"Server reinitialised with {message.author.mention} as a registered user")
    
    else:
        await util.log(f"User {message.author.name} (id={message.author.id}) attempted reinitialision of guild {message.guild.name} with id={message.guild.id} but didn't provide token ({guild_config["reset_token"]}) in channel #{message.channel.name}", guild = message.guild.id, log_type = "INITIALISATION")
        await util.pkdelay(message)
        await message.channel.send(f"Warning you are resetting server initialisation. This will delete blacklist and all registerted users/roles. To confirm use: /role reinitialise {guild_config["reset_token"]}")