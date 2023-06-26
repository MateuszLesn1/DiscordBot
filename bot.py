import random
import os
import asyncio
from itertools import cycle

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
            await bot.load_extension(f"cogs,{filename[:-3]}")
            
async def main():
    async with bot:   
        await load()
        await bot.start("MTEyMjExNTM3MDgyNDc2NTUxMA.GbOsmP.CXOVRc4k1FGsW6GR0Y2BcKOop45sF4KruqcuXE")
          
asyncio.run(main())   
 
 
#@bot.command(aliases=["8ball","question","8"])
#async def magic_eightball(ctx, *, question):
#    with open("responses.txt", "r") as file:
#        random_responses = file.readlines()
#        response = random.choice(random_responses)     
#    await ctx.send(response)
