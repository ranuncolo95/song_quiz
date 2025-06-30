import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), 'utils', '.env')
load_dotenv(dotenv_path)  # Load environment variables from .env


# Load Spotify credentials from .env
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
