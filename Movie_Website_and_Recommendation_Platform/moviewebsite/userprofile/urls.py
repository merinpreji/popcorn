from . import views
from django.urls import path
app_name = "userprofile"

urlpatterns = [
    path("profile/", views.viewprofile, name="viewprofile"),
    path("editprofile/", views.editprofile, name="editprofile"),
]
