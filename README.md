 # My first Discord Music Bot

A feature-rich Discord bot for playing and managing music in your server.

## Features

- Play music from YouTube and Spotify
- Queue management
- Playlist support (create, save, load, and manage playlists)
- User-specific playlists
- Basic playback controls (play, pause, skip, etc.)

## Commands

### Music Playback
- `!play <song>`: Play a song or add it to the queue
- `!pause`: Pause the current song
- `!resume`: Resume playback
- `!skip`: Skip the current song
- `!stop`: Stop playback and clear the queue
- `!queue`: Display the current queue

### Playlist Management
- `!playlist <url>`: Add all songs from a YouTube or Spotify playlist to the queue
- `!save_playlist <name>`: Save the current queue as a playlist
- `!load_playlist <name>`: Load a saved playlist into the queue
- `!delete_playlist <name>`: Delete a saved playlist
- `!list_playlists`: Show all your saved playlists
- `!add_to_playlist <playlist_name> <song>`: Add a song to a saved playlist
- `!remove_from_playlist <playlist_name> <index>`: Remove a song from a saved playlist
- `!show_playlist <name>`: Display the songs in a saved playlist

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Discord bot token and other necessary API keys:
   
   a. Discord Bot Token:
      - Go to the [Discord Developer Portal](https://discord.com/developers/applications)
      - Create a new application or select an existing one
      - Go to the "Bot" section and click "Add Bot"
      - Copy the token
   
   b. YouTube API Key:
      - Go to the [Google Developers Console](https://console.developers.google.com/)
      - Create a new project or select an existing one
      - Enable the YouTube Data API v3
      - Create credentials (API Key) for the YouTube Data API
   
   c. Spotify API Credentials:
      - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
      - Create a new app or select an existing one
      - Copy the Client ID and Client Secret

   After obtaining these credentials, add them to your `.env` file as described in the Configuration section.

4. Run the bot:
   ```
   python main.py
   ```

## Configuration

Create a `.env` file in the root directory with the following content:

DISCORD_TOKEN=your_discord_bot_token
YOUTUBE_API_KEY=your_youtube_api_key
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret


Replace the placeholder values with your actual API keys and tokens.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- [discord.py](https://github.com/Rapptz/discord.py)
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)

## TODO

- Add error handling for database operations
- Implement playlist sharing between users
- Add pagination for long playlists in show_playlist command
