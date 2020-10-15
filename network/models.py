from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField('User', default=None, blank=True, related_name='post_likes')

    @property
    def num_likes(self):
        return self.liked.all().count()

class Profile(models.Model):
    following = models.CharField(max_length=100,null=True, blank=True)
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='user')

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.post)
