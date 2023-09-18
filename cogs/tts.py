import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import requests
import asyncio
import time

from config import uberduck
from utils import user_in_voice, get_names, get_uuid_from_name


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

    @commands.command(aliases=["vl","voicelist"])
    async def voice_list(self, ctx):
        message = get_names(database_name)
        await ctx.author.send(f"Here is the list :\n\n{message}\n\nType .vc name to change the voice.")
    
    
    @commands.command(aliases=["vc","cv","voicechange","changevoice"])
    async def voice_change(self, ctx, name="empty_line"):
        uuid = get_uuid_from_name(database_name, name)
        if name == "empty_line":
            await ctx.author.send("You forgot the name!")
            return
        if uuid:
            self.voicemodel_uuid = uuid
            await ctx.author.send(f"Voice changed to {name}")
        else:
            await ctx.author.send(f"Voice with name {name} not found")
        

async def setup(bot):
    await bot.add_cog(Tts(bot))
    
