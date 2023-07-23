import discord
from discord import FFmpegPCMAudio
from discord.ext import commands

from config import uberduck
from time import sleep

import random
import requests


uberduck_auth = uberduck  #uberudck auth
print(requests.get("https://api.uberduck.ai/status").json())
voicemodel_uuid = "30b67b62-51a8-43db-a1b4-edafd5b4cfea" #voice model


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
         
    @commands.Cog.listener()
    async def on_ready(self):
        print("Commmands: ON ")
       
    @commands.command()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()
        
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def ping(self, ctx):
        to = ctx.author
        bot_latency = round(self.bot.latency * 1000)
        await ctx.send(f"Pong you too {to}, my latency is {bot_latency} ms")

    @commands.command()
    async def voice(self, ctx, *, text="hello, how are you"):# tts message when user forgets and argument, sadly can't make it longer, API seems to not pick up voice messages longer than 2 or 3 secs   

        audio_uuid = requests.post(
            "https://api.uberduck.ai/speak",
        json=dict(speech=text, voicemodel_uuid=voicemodel_uuid),
        auth=uberduck_auth).json()["uuid"]
        for _ in range(10):       
            output = requests.get(
                "https://api.uberduck.ai/speak-status",
                params=dict(uuid=audio_uuid),
                auth=uberduck_auth,
                                 ).json()
            print(output)
               
            if output["path"] is None:
                print("checking status")
                sleep(1) # check status every second for 10 seconds.  
                                       
            elif output["path"] != "None":
                audio_url = output["path"]
                print(audio_url)
                break

        source = FFmpegPCMAudio(audio_url, executable="ffmpeg")
        ctx.voice_client.play(source, after=None)

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
        guild = self.client.get_guild(764422667901861898) #discord id
        channel = discord.utils.get(member.guild.channels, id=1122864989900918795) #text channel id
        if guild:
            print("guild ok")
        else:
            print("guild not found")
        
        if channel is not None:
                await channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention} !  :partying_face:')
        else:
            print("no Welcome id channel")
      
class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.client=bot 
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("HelpCommand: ON")
    
    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(title="Help Commands", description="")
        help_embed.set_author(name="Serindbot",icon_url=self.client.user.avatar.url)
        help_embed.add_field(name=".join", value= "")
        help_embed.add_field(name=".leave", value="")
        help_embed.add_field(name=".ping", value="Pings bot to check it's ms")
        help_embed.add_field(name=".voice", value='TTS saying what is written after the command. Says "Hello, how are you" if left empty.')
        await ctx.send(embed= help_embed, ephemeral = True)

async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.add_cog(Welcome(bot))
    await bot.add_cog(HelpCommand(bot))
