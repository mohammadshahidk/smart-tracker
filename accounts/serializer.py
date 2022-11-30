from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers

from accounts import models as user_model

from smart_tracker.exceptions import UnauthorizedAccess
from smart_tracker.exceptions import BadRequest


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for Project user object.
    """
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        """Meta info."""
        model = user_model.ProjectUser
        fields = '__all__'

    @staticmethod
    def validate_phone(value):
        """Function to validate phone."""
        exist = user_model.ProjectUser.objects.filter(phone=value).exists()
        if exist:
            raise BadRequest('A User with this phone is already Exist')
        return value

    def create(self, validated_data):
        """
        Overriding the create method.
        """
        self.validate_phone(validated_data['phone'])
        user = super().create(validated_data)
        if 'password' in validated_data.keys():
            user.set_password(validated_data['password'])
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login the user
    """
    phone = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        """Overriding the create method."""
        user = authenticate(
            phone=validated_data['phone'],
            password=validated_data['password'])
        if not user:
            raise UnauthorizedAccess('Invalid phone or password')
        validated_data['user'] = user.id
        return user

    def to_representation(self, obj):
        """Overriding the value returned when returning th serializer."""
        data = {
            'token': obj.issue_access_token(),
            'id': obj.id,
        }
        return data


    

