# blog/models.py
# Definite the data objects for our application

from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the idea of one Article by some author'''

    #data attirbutes
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return  f'{self.title} by {self.author}'
    
    def get_comments(self):
        comments = Comment.objects.filter(article=self)
        return comments

class Comment(models.Model):
    """
    Encapsulate the idea of a Comment on an Article
    """
    article = models.ForeignKey("Article", on_delete = models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.text}'