from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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

        sm = form.save()
        files = self.request.FILES.getlist('files')
        for image in files:
            image = Image(status_message=sm, image_file=image)
            image.save()

        # delegate work to superclass method
        return super().form_valid(form)
    


## Update Forms ##
class UpdateProfileView(UpdateView):
    model=Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def form_valid(self, form):
        '''This method is called after the form is valid, before saving data to the database
        '''

        print(f'UpdateProfileView.form_valid(): form={form.cleaned_data}')
        print(f'UpdateProfileView.form_valid(): form={self.kwargs}')


        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':profile.pk}) 
    
class UpdateStatusMessageView(UpdateView):
    model=StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'status_message'
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        sm = StatusMessage.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':sm.profile.pk}) 


## Delete Form ##
class DeleteStatusMessageView(DeleteView):
    model=StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = 'status_message'

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        sm = StatusMessage.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':sm.profile.pk}) 