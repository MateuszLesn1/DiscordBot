import discord
from discord.ext import commands

class Welcome(commands.Cog) :
    def __init__(self, bot):
        self.client=bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Welcome: ON")
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(member)
        await member.send(f"hello {member} ! If you have any questions, hit me up! I can't answer them, but at least i'll listen in silence!")
        guild = self.client.get_guild(764422667901861898)                          #discord server id
        channel = discord.utils.get(member.guild.channels, id=1122864989900918795) #text channel id
        if guild:
            print("guild ok")
        else:
            print("guild not found")
        
        if channel is not None:
                await channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention} !  :partying_face:')
        else:
            print("no Welcome id channel")
      
      
async def setup(bot):
    await bot.add_cog(Welcome(bot))