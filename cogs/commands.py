import discord
from discord.ext import commands

import random

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("commands.py is ready!")
    
    @commands.command()
    async def ping(self, ctx):
        to = ctx.author
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong you too {to}, my latency is {bot_latency} ms")
        
    @commands.command(aliases=["8ball","question","8"])
    async def magic_eightball(self, ctx):
        with open("responses.txt", "r") as file:
            random_responses = file.readlines()
        response = random.choice(random_responses)     
        await ctx.send(response)
        
        

async def setup(bot):
    await bot.add_cog(Commands(bot))