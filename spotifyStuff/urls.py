from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("myStats/", views.statsPage, name="stats"),
    path("myStats/top50/<str:item_type>/<str:term_duration>/", views.top50, name="top50"),
]