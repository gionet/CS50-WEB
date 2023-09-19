from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class posts(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(blank=False)
    likes = models.ManyToManyField(User, related_name='total_likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "post": self.post,
            "likes": [user.username for user in self.likes.all()],
            "created_at": self.created_at.strftime("%b %d %Y, %I:%M %p"),
            "updated_at": self.updated_at.strftime("%b %d %Y, %I:%M %p"),
        }
    
    def __str__(self):
        return f"{self.id}: {self.username} - {self.created_at} - {self.likes}"
    
class UserProfiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    
    def __str__(self):
        return f"{self.user}"