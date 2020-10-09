from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    following = models.CharField(max_length=100,null=True, blank=True)#user ke following taki uske posts feed me dikha sake
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='user')#Sab profile objects me jakar unki following check karenge ....agr usme current user ka naam aa gya to follower ++
