import requests

class AuthUser:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        result = requests.post("https://accounts.spotify.com/api/token",
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret})
        self.auth_token = result.json()["access_token"]