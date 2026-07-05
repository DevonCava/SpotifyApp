from dotenv import load_dotenv
import os
import spotipy
from pathlib import Path
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import CacheFileHandler

load_dotenv()
client_id_env = os.getenv("CLIENTID")
client_secret_env = os.getenv("CLIENTSECRET")

REDIRECT_PORT = 8080
REDIRECT_PATH = "/callback"
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}{REDIRECT_PATH}"


def authorize_user() -> spotipy.client.Spotify:
    scope = 'user-top-read'
    cache_dir = Path("TokenCaches")
    cache_dir.mkdir(exist_ok=True)
    cache_handler = CacheFileHandler(
        cache_path=cache_dir / ".spotifycache"
    )

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id_env,
        client_secret=client_secret_env,
        redirect_uri=REDIRECT_URI,
        scope=scope,
        cache_handler=cache_handler,
    ))
    return sp


def get_me():
    sp = authorize_user()
    user = sp.current_user()
    print(user["display_name"])


def get_top_artists():
    sp = authorize_user()
    userTracks = sp.current_user_top_tracks()
    for item in userTracks["items"]:
        print(item["name"] + "\nArtist:" + item["artists"][0]["name"] + "\n")

get_top_artists()

