from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
        db_table = 'post'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created_at']
        db_table = 'comment'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.post}"

    class Meta:
        ordering = ['-created_at']
        db_table = 'like'
        unique_together = ('user', 'post')
