from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Profile) 
admin.site.register(StatusMessage) 
admin.site.register(Image) 
admin.site.register(Friend) 