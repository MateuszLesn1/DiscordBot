import discord
from discord.ext import commands
from discord import FFmpegPCMAudio

class MusicPlayer(commands.Cog):
    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.queue = []
                
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music: ON")    

    def play_next(self):
        if self.queue:
            song_url = self.queue.pop(0)
            self.voice_client.play(FFmpegPCMAudio(song_url), after=lambda e: self.play_next())

    def add_to_queue(self, song_url):
        self.queue.append(song_url)

    def clear_queue(self):
        self.queue.clear()

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))