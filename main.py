from dotenv import load_dotenv
import os
import spotipy
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional

load_dotenv()
client_id_env = os.getenv("CLIENTID")
client_secret_env = os.getenv("CLIENTSECRET")

REDIRECT_PORT = 8080
REDIRECT_PATH = "/callback"
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}{REDIRECT_PATH}"

def authorize_user() -> Optional[spotipy.client.Spotify]:
    scope = 'user-top-read'
    username = "Devon." #Adjust so that this is inputted by user on django page
    cache_dir = Path("TokenCaches")
    cache_dir.mkdir(exist_ok=True)
    cache_file = cache_dir / f".cache-{username}"
    oauth_manager = SpotifyOAuth(
        client_id=client_id_env,
        client_secret=client_secret_env,
        redirect_uri=REDIRECT_URI,
        scope=scope,
        cache_path=str(cache_file),
        username=username,
        requests_timeout=15,
    )

    sp = spotipy.Spotify(auth_manager=oauth_manager)
    if sp.current_user():
        return sp

    print("Error: Could not retrieve token.")
    return None


def get_me():
    sp = authorize_user()
    if sp is None:
        return
    user = sp.current_user()
    print(user["display_name"])


def get_top_artists():
    sp = authorize_user()
    if sp is None:
        return
    userTracks = sp.current_user_top_tracks()
    for item in userTracks["items"]:
        print(item["name"] + "\nArtist:" + item["artists"][0]["name"] + "\n")

