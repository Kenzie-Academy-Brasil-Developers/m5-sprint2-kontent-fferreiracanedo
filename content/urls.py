from django.urls import path
from . import views


urlpatterns = [
    path("kontent/", views.ContentView.as_view()),
    path("kontent/<int:content_id>/", views.ContentByIDView.as_view()),
    path("kontent/filter/", views.ContentSearchView.as_view()),
]
