from django.contrib.auth.models import User
from rest_framework import generics, viewsets, mixins
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Follow
from .serializers import RegisterSerializer, FollowSerializer
from .permissions import IsFollowOwner


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class FollowViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated, IsFollowOwner]

    def perform_create(self, serializer):
        follow_id = self.request.query_params.get('follow')
        follow = get_object_or_404(User, id=follow_id)
        if self.request.user == follow:
            raise ValidationError("You cannot follow yourself.")
        if Follow.objects.filter(follower=self.request.user,
                                 following=follow).exists():
            raise ValidationError("You are already following this user.")

        serializer.save(follower=self.request.user, following=follow)

    def get_queryset(self):
        queryset = Follow.objects.all()
        follower = self.request.query_params.get('follower')
        following = self.request.query_params.get('following')
        if follower:
            queryset = queryset.filter(follower_id=follower)
            return queryset

        if following:
            queryset = queryset.filter(following_id=following)

        return queryset
