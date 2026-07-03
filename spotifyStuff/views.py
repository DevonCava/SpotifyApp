from django.shortcuts import render, redirect
from main import authorize_user, get_top_artists
from dotenv import load_dotenv
from AuthUser import AuthUser
import os

load_dotenv()

def index(request):
    if request.method == "POST":
        client_id_env = os.getenv("CLIENTID")
        client_secret_env = os.getenv("CLIENTSECRET")
        SpotifyAuth = AuthUser(client_id_env, client_secret_env)
        authorize_user(SpotifyAuth)
        get_top_artists(SpotifyAuth)
        return render(request, "Home.html", {"message":"This is the home page"})
    return render(request, "Home.html")

def statsPage(request):
    return render(request, "stats.html")
