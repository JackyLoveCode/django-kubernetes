# core/blog/urls.py
from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("post/<slug:slug>/", views.PostDetailView.as_view(), name="detail"),
    path("category/<slug:slug>/", views.CategoryView.as_view(), name="category"),
    path("tag/<slug:slug>/", views.TagView.as_view(), name="tag"),
    path("search/", views.SearchView.as_view(), name="search"),
]
