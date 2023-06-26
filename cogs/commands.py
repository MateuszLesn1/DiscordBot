import random
import os
import asyncio
from itertools import cycle

import discord
from discord.ext import commands, tasks


class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready!")
    
    @commands.command()
    async def ping(self, ctx):
        #to = ctx.author
        bot_latency = round(self.client.latency * 1000)
        await ctx.author.send(f"Pong you too! , my latency is {bot_latency}ms")
        
        

async def setup(bot):
    await bot.add_cog(MyCog(bot))