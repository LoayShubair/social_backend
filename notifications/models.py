from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        POST = "POST", "Post"
        COMMENT = "COMMENT", "Comment"
        LIKE = "LIKE", "Like"

    # The user who receives the notification
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )

    # The user who performed the action
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_notifications"
    )

    # The related post
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=10, choices=NotificationType.choices
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor.username} {self.notification_type} on your post"
