
from django.contrib import admin
from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'show_all_views', views.ShowAllViews.as_view(), name="show_all_views"),
    path(r'', views.RandomArticleView.as_view(), name="random"),
    path(r'article/<int:pk>', views.ArticleView.as_view(), name="article"),
    ## path(r'create_comment', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment'),
    path(r'create_article', views.CreateArticleView.as_view(), name='create_article'), 

    ## authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name="login"), ## NEW
    path('logout/', auth_views.LogoutView.as_view(next_page='show_all_views'), name="logout"), ## NEW
    path('register/', views.RegistrationView.as_view(), name='register'), ## NEW
]  