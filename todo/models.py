from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


class Task(models.Model):

    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey('auth.User', related_name='tasks')
    last_updated = models.DateTimeField(auto_now_add=True)
    is_notified = models.BooleanField(default=False)


class Notification(models.Model):
    
    registration_id = models.TextField()
    title = models.TextField()
    body = models.TextField()
    last_updated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
