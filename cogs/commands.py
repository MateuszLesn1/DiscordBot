import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import requests
import asyncio

from config import uberduck



uberduck_auth = uberduck  
print(requests.get("https://api.uberduck.ai/status").json())
voicemodel_uuid = "30b67b62-51a8-43db-a1b4-edafd5b4cfea"


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
    
    async def wait_for_audio_url(self, audio_uuid):
        for _ in range(10):       
            output = requests.get(
                "https://api.uberduck.ai/speak-status",
                params=dict(uuid=audio_uuid),
                auth=uberduck_auth
            ).json()
            if output["path"] is None:       
                print("checking status")
                await asyncio.sleep(1)  # Non-blocking sleep using asyncio
            else:
                return output["path"]
        return None  # Return None if the audio URL is not available after 10 checks
    
    
    @commands.command()
    async def voice(self, ctx, *, text="hello, how are you"):
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("You need to be in a voice channel to use this command.")
            return 
        # check if the bot is already connected to any voice channel        
        if ctx.voice_client:
            # check if the bot is already in the same voice channel as the author
            if ctx.voice_client.channel == channel:                
                pass # the bot is already in the same voice channel do nothing
            else:
                # works better than the ctx.voice_client.move_to function
                await ctx.voice_client.disconnect()
                await channel.connect(timeout=None)
        # the bot is not connected to any voice channel so connect to the author's voice channel                          
        else: 
            await channel.connect(timeout=None)
            
        audio_uuid = requests.post(
            "https://api.uberduck.ai/speak",
            json=dict(speech=text, voicemodel_uuid=voicemodel_uuid),
            auth=uberduck_auth
        ).json()["uuid"]
      
        audio_url = await self.wait_for_audio_url(audio_uuid)       
        print(audio_url)
              
        if not audio_url:
            await ctx.send("Failed to generate TTS audio.")
            return
        source = FFmpegPCMAudio(audio_url, executable="ffmpeg")
        ctx.voice_client.play(source, after=None)

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
        await ctx.send(embed= help_embed, ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(Commands(bot))
    await bot.add_cog(HelpCommand(bot))
    
