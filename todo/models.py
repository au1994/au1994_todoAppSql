from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Task(models.Model):
    description = models.CharField(max_length=100)
    due_date = models.DateTimeField(null=True)
    time = models.DateTimeField(null=True)
    is_completed = models.BooleanField(default=False)
