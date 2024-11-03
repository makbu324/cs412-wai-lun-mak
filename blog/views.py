from django.shortcuts import render, redirect
import random

# Create your views here.

from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth import login ## NEW
from django.contrib.auth.models import User

class ShowAllViews(ListView):
    model = Article 
    template_name = 'blog/show_all_views.html'
    context_object_name = 'articles'

    def dispatch(self, request, *args, **kwargs):

        print(f"ShowAllView.dispatch; self.request.user={self.request.user}")

        # let the superclass version of this method do its work
        return super().dispatch(request, *args, **kwargs)

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
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view class to create a new Article instance.'''
    form_class = CreateArticleForm
    template_name = 'blog/create_article_form.html'

    def get_login_url(self)  -> str:
        '''return the URL of the login page'''
        return reverse('login')

    def form_valid(self, form):
        '''This method is called as part of the form processing.'''
        print(f'CreateArticleView.form_valid(): form.cleaned_data={form.cleaned_data}')


        # find the user who is logged in
        user = self.request.user


        # attach that user as a FK to the new Article instance
        form.instance.user = user


        # let the superclass do the real work
        return super().form_valid(form)


class RegistrationView(CreateView):
    '''Handle registration of new Users.'''

    template_name = 'blog/register.html'
    form_class = UserCreationForm # builet in from django.contrib.auth.forms

    def dispatch(self, request, *args, **kwargs):
        '''The first method that gets kicked off: '''

        ## If we received an HTTP POST, We will handle it!
        if self.request.POST:
            print(f'RegistrationView.dispatch: self.request.POST={self.request.POST}')

            # reconstruct the UserCreateForm from the POST data
            form = UserCreationForm(self.request.POST)

            if not form.is_valid():
                print(f"form.errors={form.errors}")
                
                ## Let someonebody else fix it
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save() #this will commit the insert to the database
            print(f"registrationView.dispatch: created user {user}.")

            # log the User in
            login(self.request, user)
            print(f"RegistrationView.dispatch: {user} is logged in.")

            # note for mini_fb: attach the FK user to the Profile form instance
            

            # return a message: 
            return redirect(reverse('show_all_views'))


        ## Let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)
    