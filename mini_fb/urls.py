from django.contrib import admin
from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update"),
    path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete"),
    path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name="update"),
]