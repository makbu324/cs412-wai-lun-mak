from django.contrib import admin

# Register your models here.

from .models import *

# These models are displayed on the admin page for the admin to modify/delete them.
admin.site.register(Scale) 
admin.site.register(Chord) 
admin.site.register(Song) 
admin.site.register(Artist) 
admin.site.register(UserInfo) 
admin.site.register(Recording) 