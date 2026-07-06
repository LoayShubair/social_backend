from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # JWT token generation
            refresh = RefreshToken.for_user(user)
            request.session["access_token"] = str(refresh.access_token)

            return redirect("/api/")  # ✅ التعديل المهم

        return render(request, "users/login.html", {"error": "Wrong credentials"})

    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect("/api/login/")


@login_required
def home(request):
    return render(request, "users/home.html")
