from django.db import models
from django.urls import reverse


class Profile(models.Model):
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email_address = models.EmailField(blank=False)
    # image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        return  f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        status_messages = StatusMessage.objects.filter(profile=self)
        return status_messages
    
    def get_absolute_url(self) -> str:
        return reverse('profile', kwargs={"pk": self.pk}) 
    

    def get_friends(self):
        list1 = Friend.objects.filter(profile1=self)
        list2 = Friend.objects.filter(profile2=self)
        l = list(list1) + list(list2)
        friends = []
        for frndship in l:
            if (frndship.profile1 == self):
                friends += [frndship.profile2]
            else:
                friends += [frndship.profile1]
        return friends
    
    def add_friend(self, other):
        ##print("HELLO!", self.first_name, other.first_name)
        so1 = list(Friend.objects.filter(profile1=self, profile2=other))
        so2 = list(Friend.objects.filter(profile1=other, profile2=self))
        if (so1 + so2 != [] or self == other):
            return
        else:
            ##print("success")
            new_friendship = Friend.objects.create(profile1=self, profile2=other ,timestamp = models.DateTimeField(auto_now=True))
            new_friendship.save() 
            return 
        
    def get_friend_suggestions(self):
        already_friends = self.get_friends() + [self]
        people = list(Profile.objects.all())
        suggestions = []
        for p in people:
            if not(p in already_friends):
                suggestions += [p]
        return suggestions
    
    def get_news_feed(self):
        friends = self.get_friends() + [self]
        sm_list = []
        for sm in StatusMessage.objects.all().order_by('timestamp'):
            if (sm.profile in friends):
                sm_list += [sm]
        return reversed(sm_list)
    
class StatusMessage(models.Model):
    """
    Encapsulate the idea of a Comment on an Article
    """
    profile = models.ForeignKey("Profile", on_delete = models.CASCADE)
    message  = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile} : {self.message}'
    
    def get_images(self):
        imgs = Image.objects.filter(status_message=self)
        return imgs
    
class Image(models.Model):
    """
    encapsulates the idea of an image file (not a URL) that is stored in the Django media directory
    """
    status_message = models.ForeignKey("StatusMessage", on_delete = models.CASCADE)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)


class Friend(models.Model):
    """
    Two people in a friendship!
    """
    profile1 = models.ForeignKey("Profile", on_delete = models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete = models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.profile1} & {self.profile2}'