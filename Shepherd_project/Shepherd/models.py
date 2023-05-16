from django.contrib.auth.models import User
from django.db import models


class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField()