from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, FollowViewSet

router = DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')
urlpatterns = [
    *router.urls,
    path("register/", RegisterView.as_view(), name="register"),
]


