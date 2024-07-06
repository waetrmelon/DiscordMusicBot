import discord
import os
from youtube_search import YoutubeSearch
import json 
from pytube import YouTube

from discord.ext import commands
from discord.utils import get

OriginalFolder = os.getcwd()
Files = os.listdir(OriginalFolder)

vcInstance = None

for File in Files:
    if File.endswith(".mp4"):
           os.remove(os.path.join(OriginalFolder, File))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command(name='pause', help='Pauses the song.', pass_context=True)
async def pause(ctx):
    member = ctx.message.author
    if vcInstance == None:
        await ctx.send(f'{member.mention} Failed to Pause song.')
        return
    vcInstance.pause()
    await ctx.send(f'{member.mention} Sucessfully paused song!')

@bot.command(name='resume', help='Resumes the Voice', pass_context=True)
async def resume(ctx):
    member = ctx.message.author
    if vcInstance == None:
        await ctx.send(f'{member.mention} Failed to Resume song.')
        return
    vcInstance.resume()   
    await ctx.send(f'{member.mention} Sucessfully resumed song!')

@bot.command(name='stop', help='Join the Voice', pass_context=True)
async def stop(ctx):
    member = ctx.message.author
    server = ctx.message.guild
    voice_channel = server.voice_client                
    voice_channel.stop()
    await ctx.send(f'{member.mention} Sucessfully stopped song!')

@bot.command(name='play', help='Join the Voice', pass_context=True)
async def play(ctx, *song):
    global vcInstance
    member = ctx.message.author

    name = "".join(song)
    if "https://" not in name:
        results = YoutubeSearch(name, max_results=1).to_json()
        obj = json.loads(results)
        name = "https://www.youtube.com" + obj['videos'][0]['url_suffix']
        

    await ctx.send(f'{member.mention} Attempting to join voice channel.')
    if ctx.author.voice.channel == None:
        await ctx.send(f'{member.mention} You are not in voice channel for me to join.')
        return
    
    channel = ctx.author.voice.channel
    try: 
        vc = await channel.connect()
        await ctx.send(f'{member.mention} Successfully joined voice channel.')
        await ctx.send(f'{member.mention} Now playing ' + name)
        try:
            yt = YouTube(name)
            video = yt.streams.filter(only_audio=True).first()
            video.download()
        except Exception as E:
            await ctx.send(f'{member.mention} Error: ')
            await ctx.send(E)

        audio = video.title + ".mp4"
        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=audio))
        vcInstance = vc
        
    except discord.ClientException:
        await ctx.send(f'{member.mention} Now playing ' + name)
        try:
            yt = YouTube(name)
            video = yt.streams.filter(only_audio=True).first()
            video.download()
        except Exception as E:
            await ctx.send(f'{member.mention} Error: ')
            await ctx.send(E)
            return
        audio = video.title + ".mp4"
        server = ctx.message.guild
        vc = server.voice_client    
        vc.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg/bin/ffmpeg.exe", source=audio))
        vcInstance = vc

bot.run('YOUR TOKEN HERE!')