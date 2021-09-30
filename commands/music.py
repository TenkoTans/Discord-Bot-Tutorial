import discord
import os
import urllib.request
import re
import youtube_dl

async def join(bot, ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()

async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")  

players = {}
async def play(ctx, search):
  url = await searchyt(search)
  channel = ctx.message.author.voice.channel
  voice_client = await channel.connect()
  guild = ctx.message.guild
  with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=True)
        path = str(file['title']) + "-" + str(file['id'] + ".mp3")
  voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
  voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
  await ctx.send(f'**Playing: **{url}')

async def searchyt(search):
  search_keyword=search.replace(' ', '_')
  html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
  video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
  print("https://www.youtube.com/watch?v=" + video_ids[0])
  return "https://www.youtube.com/watch?v=" + video_ids[0]

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

def endSong(guild, path):
    os.remove(path) 
