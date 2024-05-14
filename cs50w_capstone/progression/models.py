from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Posts(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.TextField(blank=False)
    timeline = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completion = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.id} : {self.username} - {self.post}"