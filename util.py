from datetime import datetime
import random
import string
import json
import os
import asyncio
import discord
import re

DIR = "D:/Eevee-bot"
LOG_FILE = f"{DIR}/log.txt"

lists_add = {"registered_roles": {"str": "registered", "log_type": "REGISTRATION"},
    "whitelist_roles": {"str": "whitelisted", "log_type": "LOG"},
    "blacklist_roles": {"str": "blacklisted", "log_type": "LOG"},}

lists_remove = {"registered_roles": {"str": "deregistered", "log_type": "REGISTRATION"},
    "whitelist_roles": {"str": "unwhitelisted", "log_type": "LOG"},
    "blacklist_roles": {"str": "unblacklisted", "log_type": "LOG"},}

def load_config(guild):
    guild_config_file = f"{DIR}/guild_configs/{guild}.json"
    if os.path.isfile(guild_config_file):
        with open(guild_config_file, 'r') as f:
            guild_config = json.load(f)
        return guild_config
    
    return None

def save_config(guild_config, guild):
    os.remove(f"{DIR}/guild_configs/{guild}.json")
    with open(f"{DIR}/guild_configs/{guild}.json", 'w') as f:
        json.dump(guild_config, f, indent=4)

async def log(log_str, guild = None, message = None, log_type = "LOG"):
    now_str = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    print(f"{now_str} {log_type}   {log_str}")
    with open(LOG_FILE, "a+") as f:
        print(f"{now_str} {log_type}   {log_str}", file=f)
    
    if guild != None:
        with open(f"{DIR}/server_logs/{guild}.txt", "a+") as f:
            print(f"{now_str} {log_type}   {log_str}", file=f)
        
        if message != None:
            guild_config = load_config(guild)
            if guild_config["log_channel"] != None:
                match = re.search(r'#([\w-]+)', log_str)
                if match:
                    channel_name = match.group(1)

                    # Try to find the text channel by name
                    channel = discord.utils.get(message.guild.text_channels, name=channel_name)
                    if channel:
                        # Replace the first occurrence of #channelname with a real mention
                        log_str = log_str.replace(f"#{channel_name}", f"<#{channel.id}>", 1)

                await message.guild.get_channel(guild_config["log_channel"]).send(f"{now_str} {log_type}   {log_str}")

def is_registered_user(message):
    guild_config = load_config(message.guild.id)

    if message.author.id in guild_config['registered_users']:
        return True
    
    return False

def is_registered_role(message):
    guild_config = load_config(message.guild.id)

    for role in message.author.roles:
        if role.id in guild_config['registered_roles']:
            return True
    
    return False

def is_registered(message):
    return is_registered_role(message) or is_registered_user(message)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def parse_roles(role_str):
    roles = role_str.split(sep = ",")
    for i, s in enumerate(roles):
        s = s.lstrip()
        roles[i] = s.rstrip()
        
    return roles

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

async def pkdelay(message):
    guild_config = load_config(message.guild.id)
    if guild_config != None:
        if guild_config["PK_mode"]:
            await asyncio.sleep(1)