from django.shortcuts import render

from rest_framework import viewsets

from accounts import serializer as user_serializer


class SignupView(viewsets.ModelViewSet):
    """View to Sign up user."""

    serializer_class = user_serializer.UserSerializer


class LoginView(viewsets.ModelViewSet):
    """View to log-in user."""
    serializer_class = user_serializer.LoginSerializer


