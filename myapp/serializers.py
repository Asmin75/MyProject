from .models import User, Post, Replies
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'created_date')


class RepliesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Replies
        fields = ('post', 'text', 'created_date')

