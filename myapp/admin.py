from django.contrib import admin
from .models import User, Post, Replies

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Replies)
