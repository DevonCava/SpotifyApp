from django.shortcuts import render, redirect
from userMethods import get_top5_tracks, get_top5_artists, get_me


def index(request):
    if request.method == "POST":
        if get_me() is not None:
            return redirect("stats")
    return render(request, "Home.html")


def statsPage(request):
#'spotifyData' is looped through via django, and must be input as a list
#Term_duration value must follow spotify API usage guide.
#Options for term duration are: 'long'(Year), 'medium'(6 months), 'short'(1 month)
    stat_cards = [
        {
            "title": "Top 5 Artists: Past Month",
            "spotifyData": get_top5_artists(term_duration="short"),
        },
{
            "title": "Top 5 Artists: Past 6 Months",
            "spotifyData": get_top5_artists(term_duration="medium"),
        },
{
            "title": "Top 5 Artists: Past Year",
            "spotifyData": get_top5_artists(term_duration="long"),
        },
        {
            "title": "Top 5 Tracks: Past Month",
            "spotifyData": get_top5_tracks(term_duration="short"),
        },
{
            "title": "Top 5 Tracks: Past 6 Months",
            "spotifyData": get_top5_tracks(term_duration="medium"),
        },
{
            "title": "Top 5 Tracks: Past Year",
            "spotifyData": get_top5_tracks(term_duration="long"),
        },
    ]

    userName = get_me()
    context = {
        "user_name": userName,
        "stat_cards": stat_cards,
    }
    return render(request, "stats.html", context)
