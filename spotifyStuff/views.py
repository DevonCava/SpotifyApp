from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from userMethods import get_top_tracks, get_top_artists, get_me


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
            "spotifyData": get_top_artists(term_duration="short", num_records=5),
            "top50_url": reverse("top50", kwargs={"item_type": "artists", "term_duration": "short"}),
        },
{
            "title": "Top 5 Artists: Past 6 Months",
            "spotifyData": get_top_artists(term_duration="medium", num_records=5),
            "top50_url": reverse("top50", kwargs={"item_type": "artists", "term_duration": "medium"}),
        },
{
            "title": "Top 5 Artists: Past Year",
            "spotifyData": get_top_artists(term_duration="long", num_records=5),
            "top50_url": reverse("top50", kwargs={"item_type": "artists", "term_duration": "long"}),
        },
        {
            "title": "Top 5 Tracks: Past Month",
            "spotifyData": get_top_tracks(term_duration="short", num_records=5),
            "top50_url": reverse("top50", kwargs={"item_type": "tracks", "term_duration": "short"}),
        },
{
            "title": "Top 5 Tracks: Past 6 Months",
            "spotifyData": get_top_tracks(term_duration="medium", num_records=5),
            "top50_url": reverse("top50", kwargs={"item_type": "tracks", "term_duration": "medium"}),
        },
{
            "title": "Top 5 Tracks: Past Year",
            "spotifyData": get_top_tracks(term_duration="long", num_records=5),
            "top50_url": reverse("top50", kwargs={"item_type": "tracks", "term_duration": "long"}),
        },
    ]

    userName = get_me()
    context = {
        "user_name": userName,
        "stat_cards": stat_cards,
    }
    return render(request, "stats.html", context)


def top50(request, item_type, term_duration):
    """Render Top 50 page with route-driven type and time-period context.

    This currently reuses Top 5 helper methods until dedicated Top 50 fetchers are added.
    """
    valid_item_types = {
        "artists": ("Artists", get_top_artists),
        "tracks": ("Tracks", get_top_tracks),
    }
    valid_terms = {
        "short": "Past Month",
        "medium": "Past 6 Months",
        "long": "Past Year",
    }

    if item_type not in valid_item_types or term_duration not in valid_terms:
        raise Http404("Invalid Top 50 filter")

    item_label, loader = valid_item_types[item_type]
    top_items = loader(term_duration=term_duration, num_records=50)

    context = {
        "top50_title": f"Top 50 {item_label}: {valid_terms[term_duration]}",
        "top50_items": top_items or [],
    }
    return render(request, "top50.html", context)
