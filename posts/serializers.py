from rest_framework import serializers

from .models import Post, Like, Comment


class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    def validate_content(self, content):
        if len(content) < 3:
            raise serializers.ValidationError(
                "Content must be at least 3 characters")
        return content

    class Meta:
        model = Post
        fields = ['id', 'content', 'username', 'created_at', 'likes_count',
                  'comments', 'comments_count', 'likes']
        read_only_fields = ['id', 'created_at', 'username', 'likes_count',
                            'comments', 'comments_count', 'likes']
        depth = 1


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'created_at', 'content']
        read_only_fields = ['user', 'post']
