import os
import asyncio
import dotenv
from dotenv import load_dotenv

import discord
from discord.ext import commands

load_dotenv()


my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='>', intents=intents)


@bot.command()
async def ping(ctx):
  await ctx.send('pong')


@bot.event
async def on_ready():
    try:
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.name == 'general':
                    await channel.send('Hello, I am a bot and I am ready to serve you!')
    except Exception as e:
        print(f'An error occurred in on_ready: {e}')
        raise


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content.startswith('hola') or message.content.startswith(
      'ola') or message.content.startswith(
          'hol') or message.content.startswith(
              'olo') or message.content.startswith('holo'):
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
    await asyncio.sleep(
        1
    )  # Añadir un retraso de 1 segundo entre las eliminaciones de mensajes

  await ctx.send(f'{amount} messages have been cleared in this channel.')


bot.run(my_secret)


