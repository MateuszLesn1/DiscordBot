import os
import asyncio

import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
intents.members = True

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
        await bot.start("MTEyMjExNTM3MDgyNDc2NTUxMA.Gf6M8f._BPi5PS9pCOfjnrnKK3fRmvVNGxdrc0gB77mt4")

asyncio.run(main())   
 

