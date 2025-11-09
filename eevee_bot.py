from datetime import datetime
import discord
import os
import dotenv
import util
import help
import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.emojis = True
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():

    # Parse changelog and 
    changelog = util.parse_changelog()
    changelog_ver = changelog[util.VERSION].split("### ")
    embed = discord.Embed(title = f"Eevee bot has been updated to {util.VERSION} on this server!", description = f"Check out the [release notes for {util.VERSION}](https://github.com/betttris13/Eevee-bot/releases/tag/{util.VERSION}) and the [full changelog](https://github.com/betttris13/Eevee-bot/blob/main/changelog.md).", colour = discord.Colour.orange())
    embed.add_field(name=f"Added:", value=changelog_ver[1].removeprefix("Added\n"))
    embed.add_field(name=f"Changed", value=changelog_ver[2].removeprefix("Changed\n"))
    embed.add_field(name=f"Fixed:", value=changelog_ver[3].removeprefix("Fixed\n"))
    embed.timestamp = datetime.now()
    embed.set_footer(text=f"Eevee bot {util.VERSION}")

    for guild in client.guilds:
        await util.log(f"Eevee bot connected to {guild.name} (id={guild.id})", guild = guild.id, log_type = "INFO")
        guild_config = util.load_config(guild.id)
        if guild_config != None:
            if guild_config["current_version"] != util.VERSION:
                guild_config["current_version"] = util.VERSION
                util.save_config(guild_config, guild.id)
                await guild.system_channel.send(embed = embed)

@client.event
async def on_guild_join(guild):
    await util.log(f"Eevee bot has joined {guild.name} (id={guild.id})", guild = guild.id, log_type = "JOIN")
    await help.join(guild)

@client.event
async def on_member_join(member):
    await help.welcome(member)

@client.event
async def on_message(message):

    # Ignore messages from self
    if message.author == client.user:
        return
    
    # Ignore webhooks
    if message.webhook_id: 
        return
    
    # Hi Eevee
    # Cute message to check bot is alive.
    if message.content.lower().startswith('hi eevee'):
        await util.pkdelay(message)
        await message.channel.send("Eevee!")

    # /Eevee bot
    # Provides bot info.
    elif message.content.lower().startswith('/eevee bot'):
        await help.bot_info(message)

    # Branch into role commands
    elif message.content.lower().startswith('/role'):
        await commands.role_commands(message)

    # Branch into emoji commands
    elif message.content.lower().startswith('/emoji'):
        await commands.emoji_commands(message)

@client.event
async def on_error(event, *args, **kwargs):
    await util.error_handle(event, *args, **kwargs)

client.run(util.TOKEN)
