from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import Follow


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    posts_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "followers_count", "following_count", "posts_count"]


class FollowSerializer(serializers.ModelSerializer):
    following = UserSerializer(read_only=True)
    follower = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "follower", "following"]
        read_only_fields = ["follower", "following"]
        depth = 1
