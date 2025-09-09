from datetime import datetime
import random
import string
import json
import os
import asyncio
import discord
import re
import dotenv

# Config settings
dotenv.load_dotenv()
DIR = str(os.getenv("DIR"))
LOG_FILE = f"{DIR}/{str(os.getenv("LOG_FILE"))}"

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

                await message.guild.get_channel(guild_config["log_channel"]).send(f"{now_str} {log_type}   {log_str}")

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
                await message.channel.send(f"Permission denied")
            return False
    
    else:
        if do_log:
            await message.channel.send(f"Server not initialised")
        return False

# Generates random alphanumeric string.
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Parses a comma separated list of roles and returns a list of role names.
def parse_roles(role_str):
    roles = role_str.split(sep = ",")
    for i, s in enumerate(roles):
        s = s.lstrip()
        roles[i] = s.rstrip()
        
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
    
    str = f""
    if added_str != "":
        str += f"The following roles were added:{added_str.removeprefix(",")}.\n"
    if failed_str != "":
        str += f"The following roles were not found:{failed_str.removeprefix(",")}.\n"
    if exists_str != "":
        str += f"The following roles already added:{exists_str.removeprefix(",")}.\n"

    return str

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
    
    str = f""
    if removed_str != "":
        str += f"The following roles were removed:{removed_str.removeprefix(",")}.\n"
    if failed_str != "":
        str += f"The following roles were not found:{failed_str.removeprefix(",")}.\n"
    if not_exists_str != "":
        str += f"The following roles were not set:{not_exists_str.removeprefix(",")}.\n"

    return str

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
    await message.channel.send(f"Server being set to use pk delay. The bot will wait 1 second before responding to allow pk proxy to send.")

# Disables pkdelay.
async def pk_off(message):
    guild_config = load_config(message.guild.id)
    guild_config["PK_mode"] = False
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) disabled pk mode in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
    await message.channel.send(f"Server being set to not use pk delay. The bot will respond immediately. Pk proxied messages may send after the bot responds.")

# Sets guild log channel.
async def log_set(message):
    guild_config = load_config(message.guild.id)
    guild_config["log_channel"] = message.channel.id
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) set log channel in channel #{message.channel.name}", guild = message.guild.id, log_type = "LOG")
    await pkdelay(message)
    await message.channel.send(f"Eevee bot set to use this channel as the log channel for this server.")

# Disables guild log channel.
async def log_off(message):
    guild_config = load_config(message.guild.id)
    guild_config["log_channel"] = None
    save_config(guild_config, message.guild.id)
    await log(f"User {message.author.name} (id={message.author.id}) disabled logging in channel #{message.channel.name}", guild = message.guild.id, log_type = "LOG")
    await pkdelay(message)
    await message.channel.send(f"Eevee bot will no longer log to this server (bot log file will not effected).")