from django.contrib import admin

# Register your models here.

from .models import *

# Register your models here.

admin.site.register(Scale) 
admin.site.register(Chord) 
admin.site.register(Song) 
admin.site.register(Artist) 
admin.site.register(UserInfo) 
admin.site.register(Recording) 