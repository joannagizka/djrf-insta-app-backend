from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Photo(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='photos')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to="media", null=False, blank=False)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
