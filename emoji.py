from datetime import datetime
import discord
import re
import aiohttp
import io
from math import ceil
import util

async def get_emoji(message):
    CUSTOM_EMOJI_PATTERN = r'<a?:\w+:(\d+)>'

    # Check if reply
    if message.reference and isinstance(message.reference.resolved, discord.Message):
        replied_message = message.reference.resolved

        # Get Emoji ids
        emoji_ids = re.findall(CUSTOM_EMOJI_PATTERN, replied_message.content)
        if not emoji_ids:
            await util.pkdelay(message)
            embed = discord.Embed(colour = discord.Colour.dark_grey())
            embed.add_field(name="No custom emojis found in message.", value="")
            embed.timestamp = datetime.now()
            embed.set_footer(text=f"Eevee bot {util.VERSION}")
            await message.channel.send(embed = embed)
            return
        
        # Get Emojis from server
        files = []
        error = False
        async with aiohttp.ClientSession() as session:
            for emoji_id in emoji_ids:
                for is_animated in [True, False]:
                    ext = 'gif' if is_animated else 'png'
                    url = f'https://cdn.discordapp.com/emojis/{emoji_id}.{ext}?v=1'
                    try:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                data = await resp.read()
                                file = discord.File(io.BytesIO(data), filename=f"{emoji_id}.{ext}")
                                files.append(file)
                                break  # Stop trying after success
                    except Exception as e:
                        error = True
        
        await util.pkdelay(message)

        if error:
            embed = discord.Embed(colour = discord.Colour.dark_grey())
            embed.add_field(name="Some emojis could not be retrieved.", value="")
            embed.timestamp = datetime.now()
            embed.set_footer(text=f"Eevee bot {util.VERSION}")
            await message.channel.send(embed = embed)

        # Send file to user
        if files:
            try:
                await util.log(f"Sending custom emojis to user {message.author.name} (id={message.author.id}) in channel #{message.channel.name}", guild = message.guild.id, message = message, log_type = "LOG")
                embed = discord.Embed(colour = discord.Colour.dark_grey())
                embed.add_field(name="Custom emojis are being sent to your DMs.", value="")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {util.VERSION}")
                await message.channel.send(embed = embed)

                batch_size = 10
                total_batches = ceil(len(files) / batch_size)

                for i in range(0, len(files), batch_size):
                    batch = files[i:i+batch_size]
                    await message.author.send(
                        content=(
                            f"Batch {i//batch_size + 1}/{total_batches} of custom emojis from the message you replied to:"
                        ),
                        files=batch
                    )
            except discord.Forbidden:
                embed = discord.Embed(colour = discord.Colour.dark_grey())
                embed.add_field(name="Unable to DM, please check your privacy settings and try again.", value="")
                embed.timestamp = datetime.now()
                embed.set_footer(text=f"Eevee bot {util.VERSION}")
                await message.channel.send(embed = embed)
        
    else:
        await util.pkdelay(message)
        embed = discord.Embed(colour = discord.Colour.dark_grey())
        embed.add_field(name="You must reply to a valid message to use this command", value="")
        embed.timestamp = datetime.now()
        embed.set_footer(text=f"Eevee bot {util.VERSION}")
        await message.channel.send(embed = embed)