from django.db import models

# Create your models here.

class Post(models.Model):
    author = models.CharField(max_length=100)
    request = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.request}'