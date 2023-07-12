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
    
def user_post_path(instance, filename):
    return "media/posts/{0}/{1}".format(instance.user_posted.username, filename)
   
class Post(models.Model):
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_post_path) # pip install pillow
    
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_getter')
    message = models.TextField()
    consumed = models.BooleanField()

class Items(models.Model):
    description = models.CharField(max_length = 200)
    store = models.CharField(max_length=100)
    price = models.FloatField()
    price_now = models.FloatField(blank=True,null = True)
    image = models.ImageField(upload_to='static/img')
