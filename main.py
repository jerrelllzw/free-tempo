import discord
from discord.ext import commands
import asyncio
import yt_dlp
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the bot token
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    """Command to join the user's voice channel."""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined {channel}!")
    else:
        await ctx.send("You need to be in a voice channel first!")

@bot.command()
async def play(ctx, playlist_url: str):
    """Command to play a YouTube playlist."""
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not vc:
        await ctx.send("I need to be in a voice channel! Use `!join` first.")
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': False,
        'quiet': True,
        'extract_flat': True
    }

    try:
        # Fetch playlist items
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(playlist_url, download=False)
            if "entries" not in info:
                await ctx.send("This doesn't seem to be a playlist.")
                return

            entries = info['entries']
            for entry in entries:
                url = entry['url']
                await play_audio(vc, url)

            await ctx.send("Finished playing the playlist!")
    except Exception as e:
        await ctx.send(f"Error: {e}")

async def play_audio(vc, url):
    """Helper function to play audio from a URL."""
    ffmpeg_options = {
        'options': '-vn'
    }
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']

    vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options))
    while vc.is_playing():
        await asyncio.sleep(1)

@bot.command()
async def leave(ctx):
    """Command to leave the voice channel."""
    vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if vc:
        await vc.disconnect()
        await ctx.send("Disconnected!")
    else:
        await ctx.send("I'm not in a voice channel!")

bot.run(BOT_TOKEN)
