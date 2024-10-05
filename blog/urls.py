
from django.contrib import admin
from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.ShowAllViews.as_view(), name="show_all"),

]