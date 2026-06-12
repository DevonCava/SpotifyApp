import requests
from dotenv import load_dotenv
import os

load_dotenv()
client_id_env = os.getenv("CLIENTID")
client_secret_env = os.getenv("CLIENTSECRET")

class AuthUser:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        result = requests.post("https://accounts.spotify.com/api/token",
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret})
        self.auth_token = result.json()["access_token"]

def get_artist_name(AuthUser):
    response = requests.get("https://api.spotify.com/v1/artists/2oM7LMPFu882oC6jSwEqjd?si=3mHZ95DaQtycbkHcmzY2ng",
                            headers={"Authorization": f"Bearer {AuthUser.auth_token}"})
    data = response.json()
    print("Artist Name:", data["name"])

SpotifyAuth = AuthUser(client_id_env, client_secret_env)
get_artist_name(SpotifyAuth)


