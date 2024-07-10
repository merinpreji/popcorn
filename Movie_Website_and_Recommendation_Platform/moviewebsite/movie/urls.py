from . import views
from django.urls import path
app_name = "movie"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("help/", views.help, name="help"),
    path("movie/<int:movie_id>/", views.moviedetail, name="moviedetail"),
    path("add/", views.add_movie, name="add_movie"),
    path("edit/<int:movie_id>", views.edit_movie, name="edit_movie"),
    path("delete/<int:movie_id>", views.del_movie, name="del_movie"),
    path("review/<int:movie_id>", views.write_review, name="write_review"),
    path("rate/<int:movie_id>", views.rate_movie, name="rate_movie"),
    path('search/', views.search_movie, name='search_movie'),
]