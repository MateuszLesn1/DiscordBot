import discord
from yt_dlp import YoutubeDL
import re

ydl_opts = {'format': 'bestaudio'} 


async def user_in_voice(ctx):
    if not ctx.author.voice:                                    # Check if the user is in a voice channel
        await ctx.send("You need to be in a voice channel to use this command.")
        return
    channel = ctx.author.voice.channel
    if ctx.voice_client:                                        # check if the bot is already connected to any voice channel    
        if ctx.voice_client.channel == channel:                 # check if the bot is already in the same voice channel as the author               
            pass                                                # the bot is already in the same voice channel do nothing
        else:                                                   # works better than the ctx.voice_client.move_to function             
            await ctx.voice_client.disconnect()
            await channel.connect(timeout=None)                           
    else:                                                       # the bot is not connected to any voice channel so connect to the author's voice channel  
        await channel.connect(timeout=None)      


async def extract_yt_info(song_url):
    with YoutubeDL(ydl_opts) as ydl:
        '''
        Currently can just play 1st song in a playlist, will add full playlist functionality soon
        '''
        if matches := re.search(r"^(.+)(?:&list=.+)", song_url,re.IGNORECASE): 
            song_url = matches.group(1)      
        info = ydl.extract_info(f"ytsearch:{song_url}", download=False)
        url = info['entries'][0]['url']
        link = info['entries'][0]['webpage_url']
        return url, link

