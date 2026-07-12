from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Post, Like, Comment
from posts.permissions import IsOwner
from posts.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.annotate(likes_count=Count('likes', distinct=True),
                                     comments_count=Count('comments', distinct=True))
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post', 'delete'], url_path='like')
    def like(self, request, pk=None):
        post = self.get_object()
        if request.method == 'POST':
            like = Like(user=self.request.user, post=post)
            like.save()
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            Like.objects.filter(
                post=post,
                user=request.user
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        post_id = self.request.query_params.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id is not None:
            post_id = self.request.query_params.get('post_id')
            post = get_object_or_404(Post, id=post_id)
            return Comment.objects.filter(post=post)
        return Comment.objects.all()
