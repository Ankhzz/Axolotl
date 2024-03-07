import os
import asyncio
import dotenv
from dotenv import load_dotenv

import nextcord
from nextcord.ext import commands

load_dotenv()

my_secret = os.environ['TOKEN']

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)

sugerencias_channel_id = 1215083256748310639
numero_sugerencia = 1


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.event
async def on_ready():
    try:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.name == 'general':
                    await channel.send('Hola jefe, ya llegue!')
    except Exception as e:
        print(f'un error ocurrio en on_ready: {e}')
        raise


@bot.event
async def on_message(message):
    global numero_sugerencia  # Indicar que estamos utilizando la variable global

    if message.author == bot.user:
        return

    if message.content.startswith('hola') or message.content.startswith('ola') or message.content.startswith(
            'hol') or message.content.startswith('olo') or message.content.startswith('holo'):
        await message.channel.send('Hola como estas?')
    await bot.process_commands(message)


@bot.command()
async def clear(ctx, amount=1):
    channel = ctx.channel
    messages = []
    async for message in channel.history(limit=amount + 1):
        messages.append(message)

    for message in messages:
        await message.delete()
        await asyncio.sleep(1)  # Añadir un retraso de 1 segundo entre las eliminaciones de mensajes

    await ctx.send(f'{amount} messages have been cleared in this channel.')


# Maneja los mensajes para detectar sugerencias
@bot.event
async def on_message(message):
    global numero_sugerencia  # Indicar que estamos utilizando la variable global

    if message.author == bot.user:
        return

    if message.channel.id == sugerencias_channel_id:
        embed = nextcord.Embed(title=f"**SUGERENCIA #{numero_sugerencia}**",
                               description=f"**Sugerencia**\n{message.content}",
                               color=0x00ff00)  # Color verde

        member = message.author

        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)

        embed.set_footer(text=f"Fecha de la Sugerencia: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}")

        embed.add_field(name="**Autor**", value=member.display_name, inline=True)

        sugerencias_channel = bot.get_channel(sugerencias_channel_id)
        if sugerencias_channel is not None:
            sent_message = await sugerencias_channel.send(embed=embed)
            await sent_message.add_reaction("✅")  # Emoji de palomita
            await sent_message.add_reaction("❌")  # Emoji de tacha

        numero_sugerencia += 1

        await message.delete()

    await bot.process_commands(message)


bot.run(my_secret)