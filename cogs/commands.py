import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @commands.Cog.listener()
    async def on_ready(self):
        print("Commmands: ON")
       
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect(timeout=None)
        
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def ping(self, ctx):
        to = ctx.author
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong you too {to}, my latency is {bot_latency} ms")
        
    """       
class HelpCommand(commands.Cog):
    def __init__(self, bot):
            self.client=bot 
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("HelpCommand: ON")
    """
async def setup(bot):
    await bot.add_cog(Commands(bot))
    #await bot.add_cog(HelpCommand(bot))
    
