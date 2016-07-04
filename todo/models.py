from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

# Create your models here.

'''
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        u = User.objects.get(username=instance)
        print u.id
        print u.username
        rand = u.password[-30:]
        print rand
        subject = "Todo App Email Verification"
        message = "http://localhost:8000/verify_account.html?id=" + str(u.id) + "&user=" + u.username + "&token=" + str(rand)
        from_email = "abhishek.upadhyay.cse12@iitbhu.ac.in"
        to_email = u.username
        send_mail(subject, message, from_email, [to_email], fail_silently=False)
'''        




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
