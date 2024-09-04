# Importing necessary modules
import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This is useful for keeping sensitive information out of the code
load_dotenv()

# Get the Discord bot token from environment variables
# Make sure to set this in your .env file
TOKEN = os.getenv('DISCORD_TOKEN')

# Get Spotify API credentials from environment variables
# These are needed for Spotify integration in our music bot
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Note: Remember to create a .env file in the same directory as this script
# and add your actual token and Spotify credentials like this:
# DISCORD_TOKEN=your_discord_token_here
# SPOTIFY_CLIENT_ID=your_spotify_client_id_here
# SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here