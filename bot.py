import os
import asyncio

import discord
from discord.ext import commands, tasks


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():   
    print("Bot is connected to discord")
    await bot.change_presence(activity=discord.Game(name=".help"))
    
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with bot:   
        await load()
        await bot.start("MTEyMjExNTM3MDgyNDc2NTUxMA.GbOsmP.CXOVRc4k1FGsW6GR0Y2BcKOop45sF4KruqcuXE")
          
asyncio.run(main())   
 

