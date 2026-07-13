from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    user = UserSerializer(read_only=True)

    def validate_content(self, content):
        if len(content) < 3:
            raise serializers.ValidationError(
                "Content must be at least 3 characters")
        return content

    class Meta:
        model = Post
        fields = ['id', 'content', 'user', 'created_at', 'likes_count',
                  'comments', 'comments_count', 'likes']
        read_only_fields = ['id', 'created_at', 'user', 'likes_count',
                            'comments', 'comments_count', 'likes']
        depth = 1


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'created_at', 'content']
        read_only_fields = ['user', 'post']
