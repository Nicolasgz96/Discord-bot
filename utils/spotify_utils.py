import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

async def get_song_info(url):
    # Extract track ID from URL
    track_id = url.split('/')[-1].split('?')[0]
    # Get track info from Spotify API
    track = sp.track(track_id)
    return {
        'title': f"{track['name']} - {track['artists'][0]['name']}",
        'url': track['external_urls']['spotify'],
    }

async def get_playlist_info(url):
    # Extract playlist ID from URL
    playlist_id = url.split('/')[-1].split('?')[0]
    # Get initial playlist tracks
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    
    # Fetch all tracks if the playlist has more than 100 songs
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    
    # Format track information
    return [{'title': f"{track['track']['name']} - {track['track']['artists'][0]['name']}", 
             'url': track['track']['external_urls']['spotify']} for track in tracks]

# TODO: Add error handling for API requests
# TODO: Implement rate limiting to avoid hitting Spotify API limits