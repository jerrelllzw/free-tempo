from discord.ext import commands
import discord
from utils import play_audio
import yt_dlp


def setup_commands(bot):
    """Register bot commands."""
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
    async def play(ctx, url: str):
        """Command to play a YouTube or Spotify link."""
        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not vc:
            await ctx.send("I need to be in a voice channel! Use `!join` first.")
            return

        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,  # Default to single video; handle playlists manually
            'quiet': True,
            'extract_flat': True
        }

        # Check if the URL is a Spotify link
        if "spotify.com" in url:
            await ctx.send("Spotify link detected, fetching audio...")

            try:
                # Use yt-dlp to extract audio from Spotify URL (yt-dlp supports Spotify)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    audio_url = info['url']

                await ctx.send(f"Now playing: {info['title']}")
                await play_audio(vc, audio_url)

            except Exception as e:
                await ctx.send(f"Error: {e}")
            return

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                if "entries" in info:  # Playlist detected
                    await ctx.send(f"Playlist detected: {info['title']}")
                    for entry in info["entries"]:
                        video_url = entry["url"]
                        await play_audio(vc, video_url)
                    await ctx.send("Finished playing the playlist!")
                else:  # Single video
                    await ctx.send(f"Now playing: {info['title']}")
                    await play_audio(vc, url)

        except Exception as e:
            await ctx.send(f"Error: {e}")

    @bot.command()
    async def leave(ctx):
        """Command to leave the voice channel."""
        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if vc:
            await vc.disconnect()
            await ctx.send("Disconnected!")
        else:
            await ctx.send("I'm not in a voice channel!")
