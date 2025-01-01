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

    @bot.command()
    async def leave(ctx):
        """Command to leave the voice channel."""
        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if vc:
            await vc.disconnect()
            await ctx.send("Disconnected!")
        else:
            await ctx.send("I'm not in a voice channel!")
