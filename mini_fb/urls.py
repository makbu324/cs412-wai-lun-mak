from django.contrib import admin
from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
]