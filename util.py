from datetime import datetime
import random
import string
import json
import os
import asyncio
import discord
import re
import dotenv
import sys
import traceback
import csv
import hashlib
from io import StringIO

# Config settings
dotenv.load_dotenv()
DIR = str(os.getenv("DIR"))
LOG_FILE = f"{DIR}/{str(os.getenv("LOG_FILE"))}"
ERROR_FILE = f"{DIR}/error_{str(os.getenv("LOG_FILE"))}"
VERSION = "pr0.1.3"

# dicts for generating log text
lists_add = {"registered_roles": {"str": "registered", "log_type": "REGISTRATION"},
    "whitelist_roles": {"str": "whitelisted", "log_type": "LOG"},
    "blacklist_roles": {"str": "blacklisted", "log_type": "LOG"},}
lists_remove = {"registered_roles": {"str": "deregistered", "log_type": "REGISTRATION"},
    "whitelist_roles": {"str": "unwhitelisted", "log_type": "LOG"},
    "blacklist_roles": {"str": "unblacklisted", "log_type": "LOG"},}

# Loads the provided guilds config
def load_config(guild):
    guild_config_file = f"{DIR}/guild_configs/{guild}.json"
    if os.path.isfile(guild_config_file):
        with open(guild_config_file, 'r') as f:
            guild_config = json.load(f)
        return guild_config
    
    return None

# Saves the provided guilds config
def save_config(guild_config, guild):
    os.remove(f"{DIR}/guild_configs/{guild}.json")
    with open(f"{DIR}/guild_configs/{guild}.json", 'w') as f:
        json.dump(guild_config, f, indent=4)

# Saves log string to log file, also logs to the guild log and then the guilds logging channel if set and message is provided.
async def log(log_str, guild = None, message = None, log_type = "LOG"):
    now_str = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    print(f"{now_str} {log_type}   {log_str}")
    with open(LOG_FILE, "a+") as f:
        print(f"{now_str} {log_type}   {log_str}", file=f)
    
    # Guild logging
    if guild != None:
        with open(f"{DIR}/server_logs/{guild}.txt", "a+") as f:
            print(f"{now_str} {log_type}   {log_str}", file=f)
        
        # Guild channel logging
        if message != None:
            guild_config = load_config(guild)
            if guild_config["log_channel"] != None:
                match = re.search(r'#([\w-]+)', log_str)
                if match:
                    channel_name = match.group(1)

                    # Attempts to replace any channel names with a channel mention.
                    channel = discord.utils.get(message.guild.text_channels, name=channel_name)
                    if channel:
                        log_str = log_str.replace(f"#{channel_name}", f"<#{channel.id}>", 1)

                embed = discord.Embed(colour = discord.Colour.orange())
                embed.add_field(name=f"{log_type} {now_str}", value=log_str)
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {VERSION}")
                await message.guild.get_channel(guild_config["log_channel"]).send(embed=embed)

# Check if user is in list of registered users.
def is_registered_user(message):
    guild_config = load_config(message.guild.id)

    if message.author.id in guild_config['registered_users']:
        return True
    
    return False

# Check if role is in list of registered roles.
def is_registered_role(message):
    guild_config = load_config(message.guild.id)

    for role in message.author.roles:
        if role.id in guild_config['registered_roles']:
            return True
    
    return False

# Check if user or their roles are registered. Throws permission log and msg if not. Also error checks for initialisation.
async def is_registered(message, do_log = True):
    guild_config_file = f"{DIR}/guild_configs/{message.guild.id}.json"
    if os.path.isfile(guild_config_file):
        if is_registered_role(message) or is_registered_user(message):
            return True
        
        else:
            if do_log:
                await log(f"User {message.author.name} (id={message.author.id}) attempted to use command {message.content} without permission in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "PERMISSION")
                await pkdelay(message)
                embed = discord.Embed(colour = discord.Colour.red())
                embed.add_field(name=f"Permission denied", value="You must be registered to use that command.")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {VERSION}")
                await message.channel.send(embed=embed)
            return False
    
    else:
        if do_log:
            await message.channel.send(embed = non_initialised())
        return False

# Generates random alphanumeric string.
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Parses a comma separated list of roles and returns a list of role names.
def parse_roles(role_str):
    reader = csv.reader(StringIO(role_str), skipinitialspace=True)
    roles = next(reader)  # reader returns a list of lists
    return roles

# Adds roles to any of the config role lists and performs error checking.
async def add_roles(message, role_str, list):
    roles = parse_roles(role_str)
    guild_config = load_config(message.guild.id)

    added_str, failed_str, exists_str = "", "", ""
    for role in roles:
        role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
        if role_obj != None:
            role_id = role_obj.id
            if role_id in guild_config[list]:
                exists_str += f", {role_obj.name}"
            else:
                added_str += f", {role_obj.name}"
                guild_config[list].append(role_id)
                await log(f"Role {role_obj.name} (id={role_id}) has been {lists_add[list]["str"]} by user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, log_type = lists_add[list]["log_type"])

        else:
            failed_str += f", {role}"

        save_config(guild_config, message.guild.id)
    
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    if added_str != "":
        embed.add_field(name=f"The following roles were added:", value=added_str.removeprefix(","))
    if failed_str != "":
        embed.add_field(name=f"The following roles were not found:", value=failed_str.removeprefix(","))
    if exists_str != "":
        embed.add_field(name=f"The following roles already added:", value=exists_str.removeprefix(","))

    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    
    return embed

# Removes roles from any of the config role lists and performs error checking.
async def remove_roles(message, role_str, list):
    roles = parse_roles(role_str)
    guild_config = load_config(message.guild.id)

    removed_str, failed_str, not_exists_str = "", "", ""
    for role in roles:
        role_obj = next((r for r in message.guild.roles if r.name.lower() == role.lower()), None)
        if role_obj != None:
            role_id = role_obj.id
            if role_id not in guild_config[list]:
                not_exists_str += f", {role_obj.name}"
            else:
                removed_str += f", {role_obj.name}"
                guild_config[list].remove(role_id)
                await log(f"Role {role_obj.name} (id={role_id}) has been {lists_remove[list]["str"]} by user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, log_type = lists_remove[list]["log_type"])

        else:
            failed_str += f", {role}"
    
        save_config(guild_config, message.guild.id)

    embed = discord.Embed(colour = discord.Colour.dark_grey())
    if removed_str != "":
        embed.add_field(name=f"The following roles were removed:", value=removed_str.removeprefix(","))
    if failed_str != "":
        embed.add_field(name=f"The following roles were not found:", value=failed_str.removeprefix(","))
    if not_exists_str != "":
        embed.add_field(name=f"The following roles were not set:", value=not_exists_str.removeprefix(","))

    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    
    return embed

# Does pk delay.
async def pkdelay(message):
    guild_config = load_config(message.guild.id)
    if guild_config != None:
        if guild_config["PK_mode"]:
            await asyncio.sleep(1)

# Enables pkdelay.
async def pk_on(message):
    guild_config = load_config(message.guild.id)
    guild_config["PK_mode"] = True
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) enabled pk mode in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    await pkdelay(message)
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    embed.add_field(name="Server being set to use pk delay.", value="The bot will wait 1 second before responding to allow pk proxy to send.")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    await message.channel.send(embed = embed)

# Disables pkdelay.
async def pk_off(message):
    guild_config = load_config(message.guild.id)
    guild_config["PK_mode"] = False
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) disabled pk mode in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    embed.add_field(name="Server being set to not use pk delay.", value="The bot will respond immediately. Pk proxied messages may send after the bot responds.")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    await message.channel.send(embed = embed)

# Sets guild log channel.
async def log_set(message):
    guild_config = load_config(message.guild.id)
    guild_config["log_channel"] = message.channel.id
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) set log channel in channel #{message.channel.name}", guild = message.guild.id, log_type = "LOG")
    await pkdelay(message)
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    embed.add_field(name = "Eevee bot set to use this channel as the log channel for this server.", value = "Log entries will now be posted here.")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    await message.channel.send(embed = embed)

# Disables guild log channel.
async def log_off(message):
    guild_config = load_config(message.guild.id)
    guild_config["log_channel"] = None
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) disabled logging in channel #{message.channel.name}", guild = message.guild.id, log_type = "LOG")
    await pkdelay(message)
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    embed.add_field(name="Eevee bot will no longer log to this server.", value="Note that bot log file will not effected")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    await message.channel.send(embed = embed)

# Error handling logic.
async def error_handle(event, *args, **kwargs):
    exc_type, exc_value, exc_tb = sys.exc_info()
    error_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    md5_hash = hashlib.md5(error_str.encode()).hexdigest()
    if event == 'on_message':
        await log(f'Unhandled exception {md5_hash} in channel #{args[0].channel.name} in command: {args[0].content}', guild = args[0].guild.id, message = args[0], log_type="ERROR")
        # await log(f'Full error: {args[0]}', guild = args[0].guild.id, log_type="ERROR")

        now_str = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        # print(f"{now_str} ERROR:\n   {error_str}-----END ERROR-----")
        with open(ERROR_FILE, "a+") as f:
            print(f"{now_str} ERROR\nError hash: {md5_hash}\n   {error_str}-----END ERROR-----\n", file=f)

    

        await pkdelay(args[0])

        embed = discord.Embed(colour = discord.Colour.red())
        embed.add_field(name="An exception has occurred.", value=f"Please notify so we can investigate and quote the following code: {md5_hash}.")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {VERSION}")
        await args[0].channel.send(embed = embed)
    
    else:
        await log(f'Unhandled exception {md5_hash}: {args[0]}', guild = args[0].guild.id, log_type="ERROR")

        now_str = datetime.now().strftime("%d-%m-%y %H:%M:%S")
        with open(ERROR_FILE, "a+") as f:
            print(f"{now_str} ERROR\nError hash: {md5_hash}\n   {error_str}-----END ERROR-----\n", file=f)

# Return server not initialised msg.
def non_initialised():
    embed = discord.Embed(colour = discord.Colour.dark_grey())
    embed.add_field(name=f"Server not initialised.", value="Please initialise the server with \"/role initialise\" and try again.")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {VERSION}")
    return embed