from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    request = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'{self.user}: {self.request}'
        else:
            return f'{self.request}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    response = models.CharField(max_length=300)
    liked_users = models.ManyToManyField(User, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user}: {self.response}'
