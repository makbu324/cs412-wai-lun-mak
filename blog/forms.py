
from django import forms
from .models import Comment, Article

class CreateCommentForm(forms.ModelForm):
    """A form to add a comment to an Article in the database"""

    class Meta:
        model = Comment 
        fields = ['author', 'text',] ## has to be called fields with an s!


class CreateArticleForm(forms.ModelForm):
    '''A form to add a new Article to the database'''
    class Meta:
        model = Article
        fields = ['author', 'title', 'text', 'image_file']