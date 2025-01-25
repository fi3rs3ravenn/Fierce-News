from django.db import models
from django.contrib.auth.models import AbstractUser


class News(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField()
    category = models.CharField(max_length=255, blank=True, default='Not Classified')
    published_date = models.DateTimeField(null=True, blank=True)
    source = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} ({self.source})'

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/' , blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    