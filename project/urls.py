from django.contrib import admin
from django.urls import path
# from quotes import views
# from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ShowAllArtists.as_view(), name=""),
    path("login/", auth_views.LoginView.as_view(template_name="project/login.html"), name="login_guitar_app"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login_guitar_app"), name="logout_guitar_app"),
    path("register/", views.RegistrationView.as_view(), name="register_guitar_app"),
    path('search_songs/', views.search_songs, name="search_songs"),
    path('show_all_artists/', views.ShowAllArtists.as_view(), name="show_all_artists"),
    path(r'song/<int:pk>', views.ShowSong.as_view(), name="song"),
    path(r'chord/<int:pk>', views.ShowChord.as_view(), name="chord"),
    path(r'artist/<int:pk>', views.ShowArtist.as_view(), name="artist"),
    path(r'user_info/<int:pk>', views.ShowUserInfo.as_view(), name="user_info"),
    path('show_all_chords/', views.ShowAllChords.as_view(), name="show_all_chords"),
    path(r'update_info/<int:pk>', views.UpdateProfileView.as_view(), name="update_info"),
    path('show_all_songs/', views.ShowAllSongs.as_view(), name="show_all_songs"),
    path('show_all_users/', views.ShowAllUsers.as_view(), name="show_all_users"),
]