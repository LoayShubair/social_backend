from rest_framework import serializers

from users.serializers import UserSerializer
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    post_content = serializers.CharField(source="post.content", read_only=True)
    user = UserSerializer(read_only=True)
    actor = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "user",
            "actor",
            "post",
            "post_content",
            "notification_type",
            "is_read",
            "created_at",
        ]

