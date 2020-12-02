from django.contrib import admin
from .models import Photo, Comment, Like

admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Like)
