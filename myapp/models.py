from _decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
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
    REQUIRED_FIELDS = ['username']

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

class Postratings(models.Model):
    rater_count = models.PositiveIntegerField(default=0, null=True)
    total = models.PositiveIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)], null=True)
    average = models.DecimalField(max_digits=5, decimal_places=3, default=Decimal(0.0))
    post = models.ForeignKey('Post', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.post


class Replies(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text