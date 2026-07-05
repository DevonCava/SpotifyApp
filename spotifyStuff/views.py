from django.shortcuts import render
from main import get_top_artists

def index(request):
    if request.method == "POST":
        get_top_artists()
        return render(request, "Home.html", {"message":"This is the home page"})
    return render(request, "Home.html")

def statsPage(request):
    return render(request, "stats.html")
