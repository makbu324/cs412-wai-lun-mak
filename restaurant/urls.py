from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'main', views.main, name="main"),
    path(r'order', views.order, name="order", ), 
    path(r'confirmation', views.confirmation, name="confirmation", ), 
]