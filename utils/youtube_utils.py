import youtube_dl

# YouTube downloader options
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

async def get_song_info(url):
    # Extract info for a single YouTube video
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info['title'],
            'url': info['url'],
        }

async def search_youtube(query):
    # Search YouTube and get info for the first result
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        return {
            'title': info['title'],
            'url': info['url'],
        }

async def get_playlist_info(url):
    # Extract info for all videos in a YouTube playlist
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return [{'title': entry['title'], 'url': entry['url']} for entry in info['entries']]

# TODO: Implement error handling for network issues or invalid URLs
# TODO: Add a function to get the duration of a video