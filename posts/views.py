from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notifications.models import Notification
from posts.models import Post, Like, Comment
from posts.permissions import IsOwner
from posts.serializers import PostSerializer, CommentSerializer, \
    PostDetailedSerializer
from users.models import Follow


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(
        likes_count=Count("likes", distinct=True),
        comments_count=Count("comments", distinct=True),
    )
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PostSerializer
        return PostDetailedSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        followers = Follow.objects.filter(
            following=self.request.user
        ).select_related("follower")

        for follow in followers:
            Notification.objects.create(
                user=follow.follower,
                actor=self.request.user,
                post=post,
                notification_type=Notification.NotificationType.POST,
            )

    @action(detail=True, methods=["post"], url_path="like")
    def like(self, request, pk=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if post.user != request.user:
            Notification.objects.create(
                user=post.user,
                actor=request.user,
                post=post,
                notification_type=Notification.NotificationType.LIKE,
            )

        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"], url_path="unlike")
    def unlike(self, request, pk=None):
        post = self.get_object()
        like = Like.objects.filter(post=post, user=request.user).first()

        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ["update", "destroy", "partial_update"]:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        post_id = self.request.query_params.get("post_id")
        post = get_object_or_404(Post, id=post_id)

        serializer.save(user=self.request.user, post=post)

        if post.user != self.request.user:
            Notification.objects.create(
                user=post.user,
                actor=self.request.user,
                post=post,
                notification_type=Notification.NotificationType.COMMENT,
            )

    def get_queryset(self):
        post_id = self.request.query_params.get("post_id")

        if post_id is not None:
            post = get_object_or_404(Post, id=post_id)
            return Comment.objects.filter(post=post)

        return Comment.objects.all()
