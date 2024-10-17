from django.shortcuts import render
import random

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse
from typing import Any

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


#form thingy
class CreateCommentView(CreateView):
    '''A view to create a Comment on an Article'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        article = Article.objects.get(pk=pk)
        # add article to context data
        context['article'] = article
        return context

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        article = Article.objects.get(pk=self.kwargs['pk'])
        return reverse('article', kwargs = {'pk':article.pk}) 
        ## note: this is not ideal, because we are redirected to the main page.

    def form_valid(self, form):
        '''This method is called after the form is valid, before saving data to the database
        '''

        print(f'CreateCommentView.form_valid(): form={form.cleaned_data}')
        print(f'CreateCommentView.form_valid(): form={self.kwargs}')

        article=Article.objects.get(pk=self.kwargs['pk'])

        form.instance.article= article

        # delegate work to superclass method
        return super().form_valid(form)
    
class CreateArticleView(CreateView):
    '''A view class to create a new Article instance.'''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def form_valid(self, form):
        '''This method is called as part of the form processing.'''
        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')

        return super().form_valid(form)