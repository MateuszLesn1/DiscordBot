import discord
from discord.ext import commands
       
class Mod_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
           
    @commands.Cog.listener()
    async def on_ready(self):
        print("mod.py is ready!")
        
    @commands.command()
    async def voice(self, ctx):
        await ctx.send(f"love you {ctx.author}", tts=True)
       
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, n=5):
        await ctx.channel.purge(limit = n)
    
async def setup(bot):
    await bot.add_cog(Mod_commands(bot))
             