import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Bot is connected to discord") 
  
@bot.command()
async def ping(ctx):
    to = ctx.author
    await ctx.author.send(f"Pong you too! {to}")
  
bot.run("MTEyMjExNTM3MDgyNDc2NTUxMA.GbOsmP.CXOVRc4k1FGsW6GR0Y2BcKOop45sF4KruqcuXE")