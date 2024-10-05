from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView 
from .models import *

class ShowAllViews(ListView):
    model = Article 
    template_name = 'blog/show_all.html'
    context_object_name = 'articles'