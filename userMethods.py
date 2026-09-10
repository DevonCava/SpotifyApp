"""Spotify API helper functions used by the Django views.
The helpers are intentionally lazy so importing this module does not trigger
Spotify OAuth during Django startup or management commands.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional
import spotipy
from dotenv import load_dotenv
from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
load_dotenv()
CLIENT_ID = os.getenv("CLIENTID")
CLIENT_SECRET = os.getenv("CLIENTSECRET")
SPOTIFY_USERNAME = os.getenv("SPOTIFY_USERNAME", "Devon.")
REDIRECT_PORT = int(os.getenv("SPOTIFY_REDIRECT_PORT", "8080"))
REDIRECT_PATH = os.getenv("SPOTIFY_REDIRECT_PATH", "/callback")
REDIRECT_URI = os.getenv(
    "SPOTIFY_REDIRECT_URI",
    f"http://127.0.0.1:{REDIRECT_PORT}{REDIRECT_PATH}",
)
TOKEN_CACHE_DIR = Path(os.getenv("TOKEN_CACHE_DIR", "TokenCaches"))
OAUTH_SCOPE = "user-top-read"
_authed_user: Optional[spotipy.client.Spotify] = None
def _build_spotify_client() -> Optional[spotipy.client.Spotify]:
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: CLIENTID and CLIENTSECRET environment variables must be set.")
        return None
    TOKEN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file = TOKEN_CACHE_DIR / f".cache-{SPOTIFY_USERNAME}"
    oauth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=OAUTH_SCOPE,
        cache_path=str(cache_file),
        username=SPOTIFY_USERNAME,
        open_browser=os.getenv("SPOTIFY_OAUTH_OPEN_BROWSER", "false").lower() in ("1", "true", "yes", "on"),
        requests_timeout=15,
    )
    client = spotipy.Spotify(auth_manager=oauth_manager)
    try:
        client.current_user()
    except SpotifyException as exc:
        print(f"Error: Could not authenticate with Spotify: {exc}")
        return None
    except Exception as exc:
        print(f"Error: Spotify authorization failed: {exc}")
        return None
    return client
def authorize_user() -> Optional[spotipy.client.Spotify]:
    global _authed_user
    if _authed_user is None:
        _authed_user = _build_spotify_client()
    return _authed_user
def get_me():
    user = authorize_user()
    if user is None:
        return None
    try:
        current_user = user.current_user()
    except Exception:
        return None
    return current_user.get("display_name")
def get_top_tracks(term_duration, num_records):
    user = authorize_user()
    if user is None:
        return []
    try:
        user_tracks = user.current_user_top_tracks(
            limit=int(num_records),
            offset=0,
            time_range=f"{term_duration}_term",
        )
    except Exception as exc:
        print(f"Error: Unable to load top tracks: {exc}")
        return []
    track_cards = []
    for item in user_tracks.get("items", []):
        album_images = item.get("album", {}).get("images", [])
        cover_art_url = album_images[0]["url"] if album_images else ""
        track_title = item.get("name", "")
        track_artist = item.get("artists", [{}])[0].get("name", "")
        track_cards.append(
            {
                "name": track_title,
                "track_title": track_title,
                "artist_name": track_artist,
                "url": item.get("external_urls", {}).get("spotify", ""),
                "image_url": cover_art_url,
            }
        )
    return track_cards
def get_top_artists(term_duration, num_records):
    user = authorize_user()
    if user is None:
        return []
    try:
        top_artists = user.current_user_top_artists(
            limit=int(num_records),
            offset=0,
            time_range=f"{term_duration}_term",
        )
    except Exception as exc:
        print(f"Error: Unable to load top artists: {exc}")
        return []
    artist_cards = []
    for item in top_artists.get("items", []):
        artist_images = item.get("images", [])
        artist_cards.append(
            {
                "name": item.get("name", ""),
                "url": item.get("external_urls", {}).get("spotify", ""),
                "image_url": artist_images[0]["url"] if artist_images else "",
            }
        )
    return artist_cards
