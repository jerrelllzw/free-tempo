import yt_dlp
import asyncio
import discord

ydl_opts = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioquality': 1,
    'outtmpl': 'downloads/%(id)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'quiet': True,
    'skip_download': True,
    'extract_flat': True,
}

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}


def setup_commands(bot):
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user}')

    @bot.command()
    async def play(ctx, url: str):
        def get_video_info(url: str):
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)

        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if not vc:
            vc = await ctx.author.voice.channel.connect()

        try:
            if vc.is_playing():
                vc.stop()

            await ctx.send("Retrieving audio data, please wait a moment.")
            info = await asyncio.to_thread(get_video_info, url)
            vc.play(discord.FFmpegPCMAudio(info["url"], **ffmpeg_opts))
            await ctx.send("Playing track.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @bot.command()
    async def pause(ctx):
        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("Paused track.")
        else:
            await ctx.send("No track is currently playing.")

    @bot.command()
    async def resume(ctx):
        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("Resumed track.")
        else:
            await ctx.send("No track is currently paused.")

    @bot.command()
    async def stop(ctx):
        vc = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if vc:
            vc.stop()
            asyncio.run_coroutine_threadsafe(vc.disconnect(), bot.loop)
            await ctx.send("Stopped music and disconnected from voice channel.")
        else:
            await ctx.send("I'm not in a voice channel!")
