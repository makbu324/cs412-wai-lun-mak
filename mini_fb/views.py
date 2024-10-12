from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import *
from .forms import *
from django.views.generic.edit import CreateView
from django.urls import reverse
from typing import Any

class ShowAllProfilesView(ListView):
    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profile' 

class ShowProfilePageView(DetailView):
    model = Profile 
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'p'
    
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

class CreateStatusMessageView(CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        profile = Profile.objects.get(pk=pk)
        # add article to context data
        context['profile'] = profile
        return context

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':profile.pk}) 
        ## note: this is not ideal, because we are redirected to the main page.

    def form_valid(self, form):
        '''This method is called after the form is valid, before saving data to the database
        '''

        print(f'CreateStatusMessageView.form_valid(): form={form.cleaned_data}')
        print(f'CreateStatusMessageView.form_valid(): form={self.kwargs}')

        profile=Profile.objects.get(pk=self.kwargs['pk'])

        form.instance.profile= profile

        # delegate work to superclass method
        return super().form_valid(form)