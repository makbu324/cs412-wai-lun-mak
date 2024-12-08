from django import forms
from .models import *

# A form that allows the user to add/change their profile pic and display name/
class UpdateUserInfoForm(forms.ModelForm):
    display_name = forms.CharField(label="Rename display name", required=True, widget=forms.Textarea(attrs={'rows': 1, 'cols': 20}))
    image_file = forms.ImageField(label="Change your avatar", required=False)

    class Meta:
        model = UserInfo 
        fields = ['display_name', 'image_file'] 