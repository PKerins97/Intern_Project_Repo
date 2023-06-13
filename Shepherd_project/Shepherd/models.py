from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField()
    date_added = models.DateTimeField(default=timezone.now)
    last_action_time = models.DateTimeField(null=True,blank=True)

class DailyLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    date_added = models.DateTimeField(default=timezone.now)
   