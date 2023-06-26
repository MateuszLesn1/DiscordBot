import random

import discord
from discord.ext import commands, tasks

from itertools import cycle


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())




@bot.event
async def on_ready():   
    print("Bot is connected to discord")
    await bot.change_presence(activity=discord.Game(name=".help"))



  
@bot.command()
async def ping(ctx):
    to = ctx.author
    bot_latency = round(bot.latency * 1000)
    await ctx.author.send(f"Pong you too! ,{to}, my latency is {bot_latency}ms")
    
@bot.command(aliases=["8ball","question","8"])
async def magic_eightball(ctx, *, question):
    with open("responses.txt", "r") as file:
        random_responses = file.readlines()
        response = random.choice(random_responses)
        
    await ctx.send(response)
    
    
    
  
bot.run("MTEyMjExNTM3MDgyNDc2NTUxMA.GbOsmP.CXOVRc4k1FGsW6GR0Y2BcKOop45sF4KruqcuXE")