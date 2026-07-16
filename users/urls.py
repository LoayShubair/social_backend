from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, FollowViewSet, UserListRetrieveViewSet

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'user', UserListRetrieveViewSet, basename='users')
urlpatterns = [
    *router.urls,
    path("register/", RegisterView.as_view(), name="register"),
]


