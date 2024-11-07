# marathon_analytics/urls.py

from django.contrib import admin
from django.urls import path
from quotes import views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # map the URL (empty string) to the view
    path(r'', views.ResultsListView.as_view(), name='home'),
    path(r'results', views.ResultsListView.as_view(), name='results'),
    path(r'result/<int:pk>', views.ResultDetailView.as_view(), name='result_detail'),
]