import asyncio
import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('music_bot')

# YouTube downloader options
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
}

# FFmpeg options for audio streaming
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -ar 44100 -ac 2 -b:a 192k -bufsize 16M'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.4):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.duration = data.get('duration')
        logger.info(f"Created YTDLSource for '{self.title}' (duration: {self.duration}s)")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        logger.info(f"Attempting to get info from: {url}")
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            if 'entries' in data:
                data = data['entries'][0]
            logger.info(f"Info obtained for: {data.get('title')} (duration: {data.get('duration')}s)")
            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
        except Exception as e:
            logger.error(f"Error getting info from {url}: {str(e)}")
            raise

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.current_song = {}
        self.play_next_song = {}
        logger.info("Music Cog initialized")

    async def play_next(self, ctx):
        # Check if bot is in a voice channel
        if ctx.voice_client is None or not ctx.voice_client.is_connected():
            logger.warning(f"Attempt to play next song without being in a voice channel in {ctx.guild}")
            return

        # Check if there are songs in the queue
        if ctx.guild.id not in self.queue or not self.queue[ctx.guild.id]:
            await ctx.send("No more songs in the queue.")
            logger.info(f"Empty queue in {ctx.guild}")
            return

        # Get the next song and play it
        current_song = self.queue[ctx.guild.id].pop(0)
        self.current_song[ctx.guild.id] = current_song
        logger.info(f"Playing '{current_song.title}' in {ctx.guild}")

        def after_playing(error):
            if error:
                logger.error(f"Error during playback: {str(error)}")
            asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

        try:
            ctx.voice_client.play(current_song, after=after_playing)
            await ctx.send(f"Now playing: {current_song.title}")
            logger.info(f"Waiting for '{current_song.title}' to finish in {ctx.guild}")
        except Exception as e:
            logger.error(f"Error playing '{current_song.title}': {str(e)}")
            await ctx.send(f"An error occurred while playing the song: {str(e)}")
            await self.play_next(ctx)

    @commands.command()
    async def play(self, ctx, *, url):
        logger.info(f"'play' command invoked by {ctx.author} in {ctx.guild} with URL: {url}")
        
        # Connect to voice channel if not already connected
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                return
        
        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                logger.info(f"Song '{player.title}' added to queue in {ctx.guild}")
                if ctx.guild.id not in self.queue:
                    self.queue[ctx.guild.id] = []
                self.queue[ctx.guild.id].append(player)
                
                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)
                else:
                    await ctx.send(f"Added to queue: {player.title}")
            except Exception as e:
                logger.error(f"Error playing {url}: {str(e)}")
                await ctx.send(f"An error occurred while trying to play the song: {str(e)}")

    # ... (rest of the commands)

async def setup(bot):
    await bot.add_cog(Music(bot))
    logger.info("Music Cog set up and added to the bot")

# TODO: Implement playlist support
# TODO: Add volume control
# TODO: Implement skip and pause commands