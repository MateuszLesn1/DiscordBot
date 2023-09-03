import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import requests
import asyncio
import time

from config import uberduck
from utils import user_in_voice


uberduck_auth = uberduck  
print(requests.get("https://api.uberduck.ai/status").json())
voicemodel_uuid = "b36fd10a-d7ce-4ccf-891f-371621112521"


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
        
    @commands.command()
    async def voice(self, ctx, *, text="hello, how are you"):
        start_time = time.time()
        await user_in_voice(ctx)

        audio_uuid = requests.post(
            "https://api.uberduck.ai/speak",
            json=dict(speech=text, voicemodel_uuid=voicemodel_uuid),
            auth=uberduck_auth
            ).json()["uuid"]

        for _ in range(10):
            output = requests.get(
                "https://api.uberduck.ai/speak-status",
                params=dict(uuid=audio_uuid),
                auth=uberduck_auth
                ).json()
            if output["path"] is None:
                print("checking status")
                await asyncio.sleep(1)
            else:
                audio_url = output["path"]
                break
        else:
            audio_url = None

        print(audio_url)
        execution_time1 = time.time() - start_time
        print(execution_time1)
        if not audio_url:
            await ctx.send("Failed to generate TTS audio.")
            return
        source = FFmpegPCMAudio(audio_url, executable="ffmpeg")
        ctx.voice_client.play(source, after=None)
        execution_time2 = time.time() - start_time
        print(execution_time2)
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
    
