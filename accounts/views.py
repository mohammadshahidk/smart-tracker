from django.shortcuts import render

from rest_framework import viewsets

from accounts import serializer as user_serializer
from accounts import models as user_models


class SignupView(viewsets.ModelViewSet):
    """View to Sign up user."""

    serializer_class = user_serializer.UserSerializer


class LoginView(viewsets.ModelViewSet):
    """View to log-in user."""
    serializer_class = user_serializer.LoginSerializer


class UserView(viewsets.ModelViewSet):
    """View to see all users"""
    queryset = user_models.ProjectUser.objects.all()
    serializer_class = user_serializer.UserSerializer


class PasswordResetView(viewsets.ModelViewSet):
    """View for password reset"""
    serializer_class = user_serializer.ResetPasswordSerializer
    queryset = user_models.ProjectUser
