from django.shortcuts import render
import random

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import *

class ShowAllViews(ListView):
    model = Article 
    template_name = 'blog/show_all_views.html'
    context_object_name = 'articles'

class RandomArticleView(DetailView):
    '''Display one Article selected at Random'''
    model = Article
    template_name = "blog/article.html"
    context_object_name = 'article'

    def get_object(self):
        '''Return one Article choosen at random'''
        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article

class ArticleView(DetailView):
    """Display one Article selected by PK (Primary key)"""
    model = Article
    template_name = "blog/article.html"
    context_object_name = 'article'