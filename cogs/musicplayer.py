import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import asyncio
from utils import user_in_voice, extract_yt_info

class MusicPlayer(commands.Cog):
    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.queue = []
        self.current_song = None
        self.MPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -af "volume=0.5"'}
        
        
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music: ON")
    
     
    @commands.command(aliases=["p","pl"])
    async def play(self, ctx, *, song_url):
        await user_in_voice(ctx)
        #make it work with playlists
        
        if not ctx.voice_client.is_playing() and self.queue:
            await self.play_next(ctx)
        elif ctx.voice_client.is_playing():
            await self.add_to_queue(ctx, song_url)
        else:
            url, link = await extract_yt_info(song_url)
            source = FFmpegPCMAudio(url, **self.MPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: asyncio.run(self.play_next(ctx)))
            self.current_song = link
            
    @commands.command(aliases=["np"])
    async def now_playing(self, ctx):
        if self.voice_client and ctx.voice_client.is_playing():     
            await ctx.send(f"Now Playing: {self.current_song}")
        else:
            await ctx.send("Nothing is currently playing.")
        
    @commands.command(aliases=["next", "n"])         
    async def play_next(self, ctx):
        if self.queue:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
            song_url = self.queue.pop(0)
                    
            url, link = await extract_yt_info(song_url) 
            source = FFmpegPCMAudio(url,**self.MPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: asyncio.run(self.play_next(ctx)))
            self.current_song = link  
            await self.now_playing(ctx)
        else:
            await ctx.send("No songs in queue")
            print("Queue is empty.")
            
            
    @commands.command()
    async def clear_queue(self, ctx):
        self.queue.clear()
        await ctx.send("Queue cleared.")
        
    @commands.command(aliases=["q","sq"])
    async def show_queue(self, ctx):
        queue_list = "\n".join(self.queue)  # convert the queue list into a string with each song on a new line
        if queue_list:
            message = f"Here is the current queue:\n{queue_list}"
        else:
            message = "The queue is currently empty."
        await ctx.author.send(message)  # send the message as a direct message to the author
       
    async def add_to_queue(self, ctx, song_url):
        url, link = await extract_yt_info(song_url)
        self.queue.append(link)
            
                        
async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))