import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import requests
import asyncio
import time
import sqlite3

from config import uberduck
from utils import user_in_voice
from voices_database import read_data


database_name = 'voices.db'
uberduck_auth = uberduck  
print(requests.get("https://api.uberduck.ai/status").json())



class Tts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.MPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -af "volume=2"'}
        self.voicemodel_uuid = "b36fd10a-d7ce-4ccf-891f-371621112521"
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("TTS: ON")
       
    @commands.command(aliases=["v"])
    async def voice(self, ctx, *, text="hello, how are you"):
        start_time = time.time()
        await user_in_voice(ctx)

        audio_uuid = requests.post(
            "https://api.uberduck.ai/speak",
            json=dict(speech=text, voicemodel_uuid=self.voicemodel_uuid),
            auth=uberduck_auth
            ).json()["uuid"]

        for _ in range(10):
            output = requests.get(
                "https://api.uberduck.ai/speak-status",
                params=dict(uuid=audio_uuid),
                auth=uberduck_auth
                ).json()
            
            if output["path"] is None:
                print("checking status.")
                await asyncio.sleep(1)
            else:
                audio_url = output["path"]
                print("worked!")
                break
        else:
            audio_url = None

        print(audio_url)
        execution_time1 = time.time() - start_time
        print(execution_time1)
        if not audio_url:
            await ctx.send("Failed to generate TTS audio.")
            return
        source = FFmpegPCMAudio(audio_url, **self.MPEG_OPTIONS)
        ctx.voice_client.play(source, after=None)
        execution_time2 = time.time() - start_time
        print(execution_time2)

    @commands.command(aliases=["vl"])
    async def voice_list(self, ctx):
        message = read_data(database_name)
        await ctx.author.send("Hey! Here is the list.")
        await ctx.author.send(message)
        await ctx.author.send("Type .vc name to change the voice.")

async def setup(bot):
    await bot.add_cog(Tts(bot))
    
