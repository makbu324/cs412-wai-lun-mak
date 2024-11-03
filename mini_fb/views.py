from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth import login ## NEW
from django.contrib.auth.models import User

class ShowAllProfilesView(ListView):
    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profile' 

class ShowProfilePageView(DetailView):
    model = Profile 
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'p'

class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        profile= Profile.objects.get(user=self.request.user)

        if request.user == profile.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('show_all_profiles')) 

    def get_login_url(self)  -> str:
        '''return the URL of the login page'''
        return reverse('login_mini_fb')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)

        # UPDATED \/ 
        profile = Profile.objects.get(user=self.request.user)
        # add article to context data
        context['profile'] = profile
        return context

    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        profile = Profile.objects.get(user=self.request.user)
        return reverse('profile', kwargs = {'pk':profile.pk}) 
        ## note: this is not ideal, because we are redirected to the main page.

    def form_valid(self, form):
        '''This method is called after the form is valid, before saving data to the database
        '''

        print(f'CreateStatusMessageView.form_valid(): form={form.cleaned_data}')
        print(f'CreateStatusMessageView.form_valid(): form={self.kwargs}')

        profile=Profile.objects.get(user=self.request.user)

        form.instance.profile= profile

        sm = form.save()
        files = self.request.FILES.getlist('files')
        for image in files:
            image = Image(status_message=sm, image_file=image)
            image.save()

        # delegate work to superclass method
        return super().form_valid(form)
    


## Update Forms ##
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model=Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        profile=Profile.objects.get(user=self.request.user)

        if request.user == profile.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('show_all_profiles')) 

    def get_login_url(self)  -> str:
        '''return the URL of the login page'''
        return reverse('login_mini_fb')

    def form_valid(self, form):
        '''This method is called after the form is valid, before saving data to the database
        '''

        print(f'UpdateProfileView.form_valid(): form={form.cleaned_data}')
        print(f'UpdateProfileView.form_valid(): form={self.kwargs}')


        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        profile = Profile.objects.get(user=self.request.user)
        return reverse('profile', kwargs = {'pk':profile.pk}) 
    
class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    model=StatusMessage
    form_class = UpdateStatusMessageForm
    template_name = "mini_fb/update_status_form.html"
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        profile=Profile.objects.get(user=self.request.user)
        sm = StatusMessage.objects.get(pk=self.kwargs['pk'])

        if sm.profile.user == profile.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('show_all_profiles'))  

    def get_login_url(self)  -> str:
        '''return the URL of the login page'''
        return reverse('login_mini_fb')
    
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        sm = StatusMessage.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':sm.profile.pk}) 


## Delete Form ##
class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    model=StatusMessage
    template_name = "mini_fb/delete_status_form.html"
    context_object_name = 'status_message'

    def dispatch(self, request, *args, **kwargs):
        profile=Profile.objects.get(user=self.request.user)
        sm = StatusMessage.objects.get(pk=self.kwargs['pk'])

        if sm.profile.user == profile.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('show_all_profiles')) 
        
    def get_login_url(self)  -> str:
        '''return the URL of the login page'''
        return reverse('login_mini_fb')

    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        sm = StatusMessage.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':sm.profile.pk}) 
    


## Add Friend ##
class CreateFriendView(LoginRequiredMixin, View):
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    def dispatch(self, request, *args, **kwargs):
        profile=Profile.objects.get(user=self.request.user)

        if request.user == profile.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('show_all_profiles')) 
        
    
    def get_login_url(self)  -> str:
        '''return the URL of the login page'''
        return reverse('login_mini_fb')
    def dispatch(self, request, *args, **kwargs):
        """redirect after creating friendship"""
        profile = Profile.objects.get(user=self.request.user)
        profile.add_friend(Profile.objects.get(pk=kwargs.get('other_pk')))
        return redirect(reverse('profile', kwargs = {'pk': profile.pk}))
    

## Friend Suggestions ##
class ShowFriendSuggestionsView(DetailView):
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    model=Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = 'p'


## Show news feed ##
class ShowNewsFeedView(DetailView):
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
    model=Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = 'p'

class RegistrationView(CreateView):
    '''Handle registration of new Users.'''

    template_name = 'mini_fb/register.html'
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

            



            ## NEW STUFF ##
            Profile.objects.create(user=user, first_name=request.POST['first_name'], last_name=request.POST['last_name'], city=request.POST['city'], email_address=request.POST['email_address'], image_file=request.FILES.get('image_file'), )
            
            # return a message: 
            return redirect(reverse('show_all_profiles'))


        ## Let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)
    
class CreateProfileView(CreateView):
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"
    def form_valid(self, form):
        '''This method is called after the form is valid, before saving data to the database
        '''

        print(f'UpdateProfileView.form_valid(): form={form.cleaned_data}')
        print(f'UpdateProfileView.form_valid(): form={self.kwargs}')


        return super().form_valid(form)
    
    def get_absolute_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs = {'pk':profile.pk}) 