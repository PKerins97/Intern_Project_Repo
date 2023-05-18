from django.contrib.auth.models import User
from django.db import models


class Points(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    points = models.IntegerField()

class DailyLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_date = models.DateField(auto_now_add=True)
    points = models.ForeignKey(Points,on_delete=models.CASCADE)
