from django.shortcuts import render, redirect
from userMethods import get_top5_tracks, get_top5_artists, get_me


def index(request):
    if request.method == "POST":
        if get_me() is not None:
            return redirect("stats")
    return render(request, "Home.html")


def statsPage(request):

    top5_artists = get_top5_artists()
    top5_tracks = get_top5_tracks()
#'spotifyData' is looped through via django, and must be input as a list
    stat_cards = [
        {
            "title": "Top 5 Artists",
            "description": "Your current favorite artists will appear here.",
            "spotifyData": top5_artists,
        },
        {
            "title": "Top 5 Tracks",
            "description": "Your most played songs will appear here.",
            "spotifyData": top5_tracks,
        },
        {
            "title": "Top Genres",
            "description": "Your most played genres will appear here.",
            "spotifyData": [{"name": "Data Placeholder", "url": "http://127.0.0.1:8000/myStats/"}],
        },
    ]

    userName = get_me()
    context = {
        "user_name": userName,
        "stat_cards": stat_cards,
    }
    return render(request, "stats.html", context)
