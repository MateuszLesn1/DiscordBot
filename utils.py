import discord
from yt_dlp import YoutubeDL
import re
import requests
import sqlite3
import logging 


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
    
  
"""

tts.py sql related functions
 
"""

def init_data(database_name):
    conn = sqlite3.connect(database_name)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS voices(
            uuid INTEGER UNIQUE,
            name TEXT     
        );
            """)
    conn.commit()
    conn.close()
    
def fetch_and_store_data(api_url, database_name):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for non-200 status codes      
        data = response.json()

        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        for dict_item in data:
            uuid = dict_item["voicemodel_uuid"]
            name = dict_item["name"]

            cursor.execute("INSERT OR IGNORE INTO voices (uuid, name) VALUES (?, ?);", (uuid, name))

        conn.commit()
        conn.close()
 
        logging.info("Data successfully fetched and stored.")
        print("")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise  
    
def get_names(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM voices;")
        
        data = cursor.fetchall()
        name_list = [] 
        for row in data:
            name = row[1]  
            name_list.append(name)
        name_message = '\n'.join(name_list)
        return name_message
                     
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        
def read_all_data(database_name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        
        select_all_data = "SELECT * FROM voices;"
        cursor.execute(select_all_data)
        
        data = cursor.fetchall()
        for row in data:
            print("UUID:", row[0])
            print("Name:", row[1])
                     
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
        
def get_uuid_from_name(database_name, name):
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        if name:
            cursor.execute("SELECT uuid from voices where name=?", (name,))
            data = cursor.fetchone()
            if data:
                return data[0]
            else:
                return None  # Name not found in the database
        else:
            return None  # Name is empty
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        conn.close()  # Make sure to close the database connection
            
                   
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    database_name = 'voices.db'
    api_url = "https://api.uberduck.ai/voices?mode=tts-basic"

    init_data(database_name)
    fetch_and_store_data(api_url, database_name)
    read_all_data(database_name)

