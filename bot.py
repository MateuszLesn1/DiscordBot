import os
import asyncio
from config import TOKEN

import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
intents.members = True

bot.remove_command("help")

@bot.event
async def on_ready():   
    print("Bot is connected to discord")
    await bot.change_presence(activity=discord.Game(name="Chilling and stuff, type .help"))
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with bot:   
        await load()
        await bot.start(TOKEN)
asyncio.run(main())   
 

