from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db import models

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=20)
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='images/', max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    photo = models.ImageField(upload_to='images/', max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    publish_date =models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Replies(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text