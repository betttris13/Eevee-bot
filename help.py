import discord
from datetime import datetime
import util

def extract_command_docs(file_path):
    command_dict = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i in range(len(lines) - 2):
        line0 = lines[i].strip()
        line1 = lines[i + 1].strip()
        line2 = lines[i + 2].strip()

        # Match pattern:
        # Line 0: "# 1 something"
        # Line 1: "# /command"
        # Line 2: "# description"
        if line0.startswith("#") and line1.startswith("# /") and line2.startswith("#"):
            vals = line0[1:].strip().split()
            pos = vals[0]
            type = vals[1]
            command = line1[2:].strip()
            description = line2[1:].strip()
            command_dict[pos] = {"type": type, "command": command, "description": description}

    return command_dict


# Generates help string and sends it to discord.
async def role_help(message):
    commands = extract_command_docs(f"{util.DIR}/commands.py")
    embed = discord.Embed(title = "**/role help documentation:**", colour = discord.Colour.blurple())
    if await util.is_registered(message, do_log = False) or await util.is_registered(message, do_log = False) == None:
        for i in range(len(commands.keys())):
            if commands[str(i+1)]["command"].startswith("/role"):
                embed.add_field(name=commands[str(i+1)]["command"], value=commands[str(i+1)]["description"])
    else:
        for i in range(len(commands.keys())):
            if commands[str(i+1)]["command"].startswith("/role") and commands[str(i+1)]["type"] == 'any':
                embed.add_field(name=commands[str(i+1)]["command"], value=commands[str(i+1)]["description"])
    
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")

    await util.pkdelay(message)
    await message.channel.send(embed=embed)

# Generates help string and sends it to discord.
async def emoji_help(message):
    commands = extract_command_docs(f"{util.DIR}/commands.py")
    embed = discord.Embed(title = "**/emoji help documentation:**", colour = discord.Colour.blurple())
    if await util.is_registered(message, do_log = False) or await util.is_registered(message, do_log = False) == None:
        for i in range(len(commands.keys())):
            if commands[str(i+1)]["command"].startswith("/emoji"):
                embed.add_field(name=commands[str(i+1)]["command"], value=commands[str(i+1)]["description"])
    else:
        for i in range(len(commands.keys())):
            if commands[str(i+1)]["command"].startswith("/emoji") and commands[str(i+1)]["type"] == 'any':
                embed.add_field(name=commands[str(i+1)]["command"], value=commands[str(i+1)]["description"])
    
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")

    await util.pkdelay(message)
    await message.channel.send(embed=embed)

# Generates list of available roles on the guild and sends it to discord.
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
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.add_field(name="**Available roles:**", value=available_roles)
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")
    await message.channel.send(embed=embed)

# Outputs pot info
async def bot_info(message):
    embed = discord.Embed(title = f"Eevee bot {util.VERSION}", colour = discord.Colour.blurple())
    embed.add_field(name=f"For help with role management use:", value="/role help")
    embed.add_field(name=f"For this message use:", value="/Eevee bot")
    embed.add_field(name=f"To get a cute response use:", value="Hi Eevee")
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")
    await util.pkdelay(message)
    await message.channel.send(embed = embed)

# Generates list of roles the user has that are available discord.
async def list_roles_user(message):
    guild_config = util.load_config(message.guild.id)
    roles = ""

    if guild_config["blacklist_mode"]:
        for role in message.author.roles:
            if role.id == message.guild.id:
                continue
            
            if role.id not in guild_config["blacklist_roles"]:
                roles += f", {role.name}"
    else:
        for role in message.guild.roles:
            if role.id == message.guild.id:
                continue

            if role.id in guild_config["whitelist_roles"]:
                roles += f", {role.name}"

    await util.pkdelay(message)
    embed = discord.Embed(colour = discord.Colour.blurple())
    embed.add_field(name="**Your roles:**", value=roles.removeprefix(", "))
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")
    await message.channel.send(embed=embed)

# Outputs pot info
async def welcome(member):
    if member.guild.system_channel and member.guild.system_channel.permissions_for(member.guild.me).send_messages:
        embed = discord.Embed(title = f"Welcome to {member.guild.name}!!", colour = discord.Colour.blurple())
        embed.add_field(name=f"For help with role management use:", value="/role help")
        embed.add_field(name=f"For this message use:", value="/Eevee bot")
        embed.add_field(name=f"To get a cute response use:", value="Hi Eevee")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await member.guild.system_channel.send(embed = embed)