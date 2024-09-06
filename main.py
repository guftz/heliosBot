# type: ignore

import os

import discord
from discord.ext import commands 

from dotenv import load_dotenv 
load_dotenv('.env')


bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user.name} is online!")

@bot.event
async def on_connect():
    if bot.auto_sync_commands:
        await bot.sync_commands()
    print(f"{bot.user.name} connected.")


# Command on Cooldown Trigger
@bot.event
async def on_application_command_error(
    ctx: discord.ApplicationContext, error: discord.DiscordException
):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown.")
    else:
        raise error  
    
    
# Loading the Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith('_'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'{filename[:-3].capitalize()} cog loaded')



bot.run(os.getenv('BOT_TOKEN'))