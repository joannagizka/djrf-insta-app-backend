from django.contrib import admin
from .models import Photo, Comment, Like, Observation

admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Observation)
