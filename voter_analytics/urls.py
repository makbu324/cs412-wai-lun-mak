from django.urls import path
from quotes import views
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # map the URL (empty string) to the view
    path(r'', views.VotersListView.as_view(), name='voters'),
    path(r'voters', views.VotersListView.as_view(), name='voters'),
    path(r'voter/<int:pk>', views.VoterView.as_view(), name='show_voter'),
    path(r'graph', views.GraphListView.as_view(), name='graph'),
]