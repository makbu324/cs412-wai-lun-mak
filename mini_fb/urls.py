from django.contrib import admin
from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path(r'', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'show_all_profiles', views.ShowAllProfilesView.as_view(), name="show_all_profiles"),
    path(r'create_profile', views.CreateProfileView.as_view(), name="create_profile"),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
    path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name="delete"),
    path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name="update_status"),

    ## CHANGED FIRST FIVE LINKS
    path(r'status/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    path(r'profile/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path(r'profile/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name="add_new_friend"),
    path(r'profile/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name="friend_suggestions"),
    path(r'profile/news_feed', views.ShowNewsFeedView.as_view(), name="news_feed"),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name="login_mini_fb"),
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name="logout_mini_fb"), 
    path('register/', views.RegistrationView.as_view(), name='register_mini_fb'),
]