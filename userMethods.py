from dotenv import load_dotenv
import os
import spotipy
from pathlib import Path
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional
from collections import Counter

load_dotenv()
client_id_env = os.getenv("CLIENTID")
client_secret_env = os.getenv("CLIENTSECRET")

REDIRECT_PORT = 8080
REDIRECT_PATH = "/callback"
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}{REDIRECT_PATH}"

#--Authorizes user utilizing spotify's OAuth2.0 flow and returns a Spotify client object if successful,
#   otherwise returns None.
# This method runs before any other methods in order to ensure the "authedUser" object is initialized
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

authedUser = authorize_user()

def get_me():
    if authedUser is None:
        return None
    user = authedUser.current_user()
    return user["display_name"]


def get_top5_tracks(term_duration):
    if authedUser is None:
        return None
    trackLists = []
    trackLinks = []
    userTracks = authedUser.current_user_top_tracks(limit=5, offset=0, time_range=f"{term_duration}_term")
    for item in userTracks["items"]:
        trackLists.append(item["name"] + " - " + item["artists"][0]["name"])
        trackLinks.append(item["external_urls"]["spotify"])
    track_cards = [
        {"name": name, "url": url}
        for name, url in zip(trackLists, trackLinks)
    ]
    return track_cards

def get_top5_artists(term_duration):
    if authedUser is None:
        return None
    artistLists = []
    artistLinks = []
    topArtists = authedUser.current_user_top_artists(limit=5, offset=0, time_range=f"{term_duration}_term")
    for item in topArtists["items"]:
        artistLists.append(item["name"])
        artistLinks.append(item["external_urls"]["spotify"])
    artist_cards = [
        {"name": name, "url": url}
        for name, url in zip(artistLists, artistLinks)
    ]
    return artist_cards
