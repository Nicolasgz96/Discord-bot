import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('music_bot.db')
c = conn.cursor()

# Create the playlists table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS playlists
             (id INTEGER PRIMARY KEY, name TEXT, user_id INTEGER, songs TEXT)''')

# Function to save a playlist
def save_playlist(name, user_id, songs):
    songs_json = json.dumps(songs)
    c.execute("INSERT OR REPLACE INTO playlists (name, user_id, songs) VALUES (?, ?, ?)",
              (name, user_id, songs_json))
    conn.commit()

# Function to load a playlist
def load_playlist(name, user_id):
    c.execute("SELECT songs FROM playlists WHERE name = ? AND user_id = ?", (name, user_id))
    result = c.fetchone()
    if result:
        return json.loads(result[0])
    return None

# Function to delete a playlist
def delete_playlist(name, user_id):
    c.execute("DELETE FROM playlists WHERE name = ? AND user_id = ?", (name, user_id))
    conn.commit()

# Function to get all playlists for a user
def get_user_playlists(user_id):
    c.execute("SELECT name FROM playlists WHERE user_id = ?", (user_id,))
    return [row[0] for row in c.fetchall()]

# Function to add a song to a playlist
def add_song_to_playlist(name, user_id, song):
    playlist = load_playlist(name, user_id)
    if playlist is not None:
        playlist.append(song)
        save_playlist(name, user_id, playlist)
        return True
    return False

# Function to remove a song from a playlist
def remove_song_from_playlist(name, user_id, index):
    playlist = load_playlist(name, user_id)
    if playlist is not None and 0 <= index < len(playlist):
        del playlist[index]
        save_playlist(name, user_id, playlist)
        return True
    return False

# TODO: Add error handling and connection closing