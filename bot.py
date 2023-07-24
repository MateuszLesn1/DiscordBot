import os
import asyncio

from config import TOKEN

import discord
from discord.ext import commands
from discord.utils import get

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
intents.members = True

bot.remove_command("help")

@bot.event
async def on_ready():   
    print("Bot is connected to discord")
    await bot.change_presence(activity=discord.Game(name="Chilling and stuff, type .help"))

@bot.event
async def on_raw_reaction_add(reaction):
    emoji = reaction.emoji.name
    if reaction.message_id == 1132628800010719303: # ID of message, to which reacting, will assign roles based on rules below 
        if emoji =="👋":
            get_role = get(reaction.member.guild.roles, name="Hey")
            await reaction.member.add_roles(get_role)
                          
        elif emoji == "🥷":
            get_role = get(reaction.member.guild.roles, name="Check")
            await reaction.member.add_roles(get_role)
                   
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with bot:   
        await load()
        await bot.start(TOKEN)
        
asyncio.run(main())   
 

