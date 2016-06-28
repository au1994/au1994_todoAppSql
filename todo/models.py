from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Task(models.Model):
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='tasks')
    last_updated = models.DateTimeField(auto_now_add=True)
