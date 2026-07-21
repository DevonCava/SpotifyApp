from django.shortcuts import render, redirect
from userMethods import get_me


def index(request):
    if request.method == "POST":
        if get_me() is not None:
            return redirect("stats")
    return render(request, "Home.html")


def statsPage(request):

    stat_cards = [
        {
            "title": "Top 5 Artists",
            "description": "Your current favorite artists will appear here.",
            "spotifyData": "Data coming soon",
        },
        {
            "title": "Top 5 Tracks",
            "description": "Your most played songs will appear here.",
            "spotifyData": "Data coming soon",
        },
        {
            "title": "Listening Time",
            "description": "Your total listening time will appear here.",
            "spotifyData": "Data coming soon",
        },
        {
            "title": "Top Genres",
            "description": "Your most played genres will appear here.",
            "spotifyData": "Data coming soon",
        },
    ]

    userName = get_me()
    context = {
        "user_name": userName,
        "stat_cards": stat_cards,
    }
    return render(request, "stats.html", context)
