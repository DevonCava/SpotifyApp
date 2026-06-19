import requests
from AuthUser import AuthUser
from dotenv import load_dotenv
import os

import http.server
import socketserver
import threading
import webbrowser
import urllib.parse as urlparse
import requests
import time
import secrets

load_dotenv()
client_id_env = os.getenv("CLIENTID")
client_secret_env = os.getenv("CLIENTSECRET")

REDIRECT_PORT = 8000
REDIRECT_PATH = "/callback"
REDIRECT_URI = f"http://127.0.0.1:{REDIRECT_PORT}{REDIRECT_PATH}"


def get_artist_name(AuthUser, artist_id):
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}",
        headers={"Authorization": f"Bearer {AuthUser.auth_token}"},
    )
    data = response.json()
    print("Artist Name:", data["name"])


def get_me(AuthUser):
    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers={"Authorization": f"Bearer {AuthUser.auth_token}"},
    )
    data = response.json()
    print(data)


def get_top_artists(AuthUser):
    response = requests.get(
        "https://api.spotify.com/v1/me/top/artists?limit=5&offset=0",
        headers={"Authorization": f"Bearer {AuthUser.auth_token}"},
    )
    data = response.json()
    for artist in data["items"]:
        print(artist["name"])


# python
def authorize_user(
    auth_user,
    scopes=("user-top-read", "user-read-recently-played", "user-read-private"),
):
    """
    Opens a browser to let the user authorize the application, captures the code
    on the local callback, exchanges it for tokens and sets:
      auth_user.auth_token
      auth_user.refresh_token
    """
    client_id = client_id_env
    client_secret = client_secret_env
    state = secrets.token_urlsafe(16)
    scope_str = " ".join(scopes)

    REDIRECT_HOST = "127.0.0.1"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "scope": scope_str,
        "redirect_uri": f"http://{REDIRECT_HOST}:{REDIRECT_PORT}{REDIRECT_PATH}",
        "state": state,
        "show_dialog": "true",
    }
    auth_url = "https://accounts.spotify.com/authorize?" + urlparse.urlencode(params)

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse.urlparse(self.path)
            if parsed.path != REDIRECT_PATH:
                self.send_response(404)
                self.end_headers()
                return
            qs = urlparse.parse_qs(parsed.query)
            code = qs.get("code", [None])[0]
            recv_state = qs.get("state", [None])[0]

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            if code and recv_state == state:
                self.wfile.write(
                    b"<html><body><h1>Authorization received. You can close this window.</h1></body></html>"
                )
                self.server.auth_code = code
                # shutdown the server from a background thread to avoid deadlock
                threading.Thread(target=self.server.shutdown, daemon=True).start()
            else:
                self.wfile.write(
                    b"<html><body><h1>Authorization failed or state mismatch.</h1></body></html>"
                )
                self.server.auth_code = None

        def log_message(self, format, *args):
            return

    # Use ThreadingTCPServer and bind explicitly to the same host used in REDIRECT_URI
    class ThreadedServer(socketserver.ThreadingTCPServer):
        allow_reuse_address = True

    httpd = ThreadedServer((REDIRECT_HOST, REDIRECT_PORT), CallbackHandler)
    httpd.auth_code = None

    server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    server_thread.start()

    webbrowser.open_new_tab(auth_url)

    # Wait for the auth code (with a reasonable timeout)
    timeout = 30
    poll_interval = 0.5
    waited = 0.0
    while waited < timeout and httpd.auth_code is None:
        time.sleep(poll_interval)
        waited += poll_interval

    # ensure server is stopped
    try:
        httpd.shutdown()
    except Exception:
        pass
    httpd.server_close()

    code = httpd.auth_code
    if not code:
        raise RuntimeError("Authorization failed or timed out.")

    # Exchange code for tokens
    token_url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"http://{REDIRECT_HOST}:{REDIRECT_PORT}{REDIRECT_PATH}",
    }
    resp = requests.post(token_url, data=data, auth=(client_id, client_secret))
    resp.raise_for_status()
    token_data = resp.json()

    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    if not access_token:
        raise RuntimeError("Failed to obtain access token from Spotify.")

    auth_user.auth_token = access_token
    auth_user.refresh_token = refresh_token

    return auth_user


SpotifyAuth = AuthUser(client_id_env, client_secret_env)
authorize_user(SpotifyAuth)
get_top_artists(SpotifyAuth)
