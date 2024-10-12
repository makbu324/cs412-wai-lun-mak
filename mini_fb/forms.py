from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):

    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email_address = forms.EmailField(label="Email", required=True)
    image_url = forms.URLField(label="Image URL", required=True)

    class Meta:
        model = Profile 
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_url', ] ## has to be called fields with an s!

class CreateStatusMessageForm(forms.ModelForm):
    message = forms.CharField(label="How you Feelin'? ", required=True)

    class Meta:
        model = StatusMessage 
        fields = ['message', ]
        