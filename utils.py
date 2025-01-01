import discord
import yt_dlp
import asyncio


async def play_audio(vc, url):
    """Helper function to play audio from a URL."""
    ffmpeg_options = {
        'options': '-vn'  # Excludes video; for audio-only playback
    }
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']

        vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_options))
        while vc.is_playing():
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error in play_audio: {e}")
