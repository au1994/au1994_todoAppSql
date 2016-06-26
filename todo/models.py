from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='tasks')

