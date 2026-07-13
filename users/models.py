from django.contrib.auth.models import User
from django.db import models


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following_users'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} started following {self.following.username}"

    class Meta:
        ordering = ["-created_at"]
        unique_together = ('follower', 'following')
