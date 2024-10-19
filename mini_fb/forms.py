from django import forms
from .models import *

class CreateProfileForm(forms.ModelForm):

    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    city = forms.CharField(label="City", required=True)
    email_address = forms.EmailField(label="Email", required=True)
    image_file = forms.ImageField(label="Image Upload", required=True)

    class Meta:
        model = Profile 
        fields = ['first_name', 'last_name', 'city', 'email_address', 'image_file', ] ## has to be called fields with an s!

class CreateStatusMessageForm(forms.ModelForm):
    message = forms.CharField(label="How you Feelin'? ", required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = StatusMessage 
        fields = ['message', ]
        
class UpdateProfileForm(forms.ModelForm):
    city = forms.CharField(label="City", required=True)
    email_address = forms.EmailField(label="Email", required=True)
    image_file = forms.ImageField(label="Image Upload", required=True)

    class Meta:
        model = Profile 
        fields = ['city', 'email_address', 'image_file', ] 

class UpdateStatusMessageForm(forms.ModelForm):
    message = forms.CharField(label="How you Feelin'? ", required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    class Meta:
        model = StatusMessage 
        fields = ['message', ] 