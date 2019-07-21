from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=50,
        unique=True
    )

    password = models.CharField(
        max_length=50
    )

    full_name = models.CharField(
        max_length=50
    )

    models = models.ImageField(upload_to='profile_image', blank=True)

    def __str__(self):
        return self.username


class Post(models.Model):
    title = models.CharField(
        max_length=50
    )

    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    body = models.TextField()

    date = models.DateField(default=timezone.now)


    def __str__(self):
        return self.title
