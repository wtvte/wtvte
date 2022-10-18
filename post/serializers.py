from django.contrib.auth.models import User
from rest_framework import serializers
from post.models import Post
from author.serializers import UserSerializer


class PostSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'image']
        read_only_fields = ['user']


