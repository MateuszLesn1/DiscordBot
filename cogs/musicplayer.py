import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp


class MusicPlayer(commands.Cog):
    def __init__(self, voice_client):
        self.voice_client = voice_client
        self.queue = []    
        self.ydl_opts = {'format': 'bestaudio'}  # use yt_dlp to fetch the URL of the song from YouTube
        self.MPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        
             
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music: ON")
     
    @commands.command(aliases=["p","pl"])
    async def play(self, ctx, *, song_url):
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
        
        self.add_to_queue(song_url)
        
        # check if the bot is not currently playing anything and there are songs in the queue       
        if not ctx.voice_client.is_playing() and self.queue:
            await self.play_next() # start playing the next song in the queue

        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{song_url}", download=False)
            url = info['entries'][0]['url']
            
        source = discord.FFmpegPCMAudio(url, **self.MPEG_OPTIONS)
        ctx.voice_client.play(source) # play the song from the bot in the voice channel
        
    '''       
    @commands.command()
    async def now_playing(self, ctx):
        if self.voice_client:
            current_song = self.queue[0] if self.queue else "No songs in the queue"
            await ctx.send(f"Now Playing: {current_song}")
        else:
            await ctx.send("Nothing is currently playing.")     
        '''
    @commands.command(aliases=["next", "n"])         
    async def play_next(self, ctx):
        if self.queue:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()

            song_url = self.queue.pop(0)
            ("songurl",song_url)
       
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch:{song_url}", download=False)
                url = info['entries'][0]['url']
         
            source = discord.FFmpegPCMAudio(url,**self.MPEG_OPTIONS)
            ctx.voice_client.play(source, after=lambda _: self.play_next())
            print(f"Playing next song: {song_url}")
        else:
            print("Queue is empty.")
            
    @commands.command(aliases=["add"])
    async def add_to_queue(self, ctx, song_url):
        self.queue.append(song_url)
        await ctx.send(f"Added to queue: {song_url}")
        
    @commands.command()
    async def clear_queue(self, ctx):
        self.queue.clear()
        await ctx.send("Queue cleared.")

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))