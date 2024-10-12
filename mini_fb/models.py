from django.db import models
from django.urls import reverse


class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return  f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
    def get_absolute_url(self) -> str:
        return reverse('profile', kwargs={"pk": self.pk}) 
    
class StatusMessage(models.Model):
    """
    Encapsulate the idea of a Comment on an Article
    """
    profile = models.ForeignKey("Profile", on_delete = models.CASCADE)
    message  = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile} : {self.message}'