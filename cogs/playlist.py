from discord.ext import commands
from utils import youtube_utils, spotify_utils, database

class Playlist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playlist(self, ctx, url):
        try:
            # Determine the source of the playlist (YouTube or Spotify)
            if 'youtube.com' in url or 'youtu.be' in url:
                songs = await youtube_utils.get_playlist_info(url)
            elif 'spotify.com' in url:
                songs = await spotify_utils.get_playlist_info(url)
            else:
                await ctx.send("Invalid playlist URL.")
                return

            # Add songs to the queue
            music_cog = self.bot.get_cog('Music')
            for song in songs:
                music_cog.queue.append(song)
            
            await ctx.send(f"Added {len(songs)} songs to the queue.")
            
            # Start playing if not already playing
            if not music_cog.voice_client.is_playing():
                await music_cog.play_next(ctx)
        except Exception as e:
            await ctx.send(f"Error adding playlist: {str(e)}")

    @commands.command()
    async def save_playlist(self, ctx, name):
        music_cog = self.bot.get_cog('Music')
        if not music_cog.queue:
            await ctx.send("The queue is empty. Nothing to save.")
            return
        
        database.save_playlist(name, ctx.author.id, music_cog.queue)
        await ctx.send(f"Playlist '{name}' saved successfully.")

    @commands.command()
    async def load_playlist(self, ctx, name):
        songs = database.load_playlist(name, ctx.author.id)
        if not songs:
            await ctx.send(f"Playlist '{name}' not found.")
            return
        
        music_cog = self.bot.get_cog('Music')
        music_cog.queue.extend(songs)
        await ctx.send(f"Playlist '{name}' loaded. Added {len(songs)} songs to the queue.")

    @commands.command()
    async def delete_playlist(self, ctx, name):
        database.delete_playlist(name, ctx.author.id)
        await ctx.send(f"Playlist '{name}' deleted.")

    @commands.command()
    async def list_playlists(self, ctx):
        playlists = database.get_user_playlists(ctx.author.id)
        if playlists:
            playlist_list = "\n".join(playlists)
            await ctx.send(f"Your playlists:\n{playlist_list}")
        else:
            await ctx.send("You don't have any saved playlists.")

    @commands.command()
    async def add_to_playlist(self, ctx, playlist_name, *, song):
        if database.add_song_to_playlist(playlist_name, ctx.author.id, song):
            await ctx.send(f"Song '{song}' added to playlist '{playlist_name}'.")
        else:
            await ctx.send(f"Couldn't add the song. Make sure the playlist '{playlist_name}' exists.")

    @commands.command()
    async def remove_from_playlist(self, ctx, playlist_name, index: int):
        if database.remove_song_from_playlist(playlist_name, ctx.author.id, index - 1):
            await ctx.send(f"Song removed from playlist '{playlist_name}'.")
        else:
            await ctx.send(f"Couldn't remove the song. Make sure the playlist '{playlist_name}' exists and the index is valid.")

    @commands.command()
    async def show_playlist(self, ctx, name):
        songs = database.load_playlist(name, ctx.author.id)
        if songs:
            song_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(songs)])
            await ctx.send(f"Songs in playlist '{name}':\n{song_list}")
        else:
            await ctx.send(f"Playlist '{name}' not found or is empty.")

async def setup(bot):
    await bot.add_cog(Playlist(bot))

# TODO: Add error handling for database operations
# TODO: Implement playlist sharing between users
# TODO: Add pagination for long playlists in show_playlist command