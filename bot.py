import token
from discord.ext import commands
import os
import discord
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!',help_command=None,intents=intents)


@bot.command()
async def unload(ctx,ext):
    bot.unload_extension(f"cogs.{ext}")
    
@bot.command()
async def load(ctx,ext):
    bot.load_extension(f"cogs.{ext}")
    
@bot.command()
async def reload(ctx):
    bot.reload_extension("cogs.user_commands")
    
    

for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')



bot.run(os.getenv('TOKEN'))
