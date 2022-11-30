from django.conf import settings
from rest_framework import permissions

from smart_tracker.exceptions import UnauthorizedAccess
from smart_tracker.exceptions import BadRequest
from smart_tracker.exceptions import AccessForbidden

from accounts.models import AccessToken


class IsAuthenticated(permissions.BasePermission):
    """
    Check if the user is authenticated.

    Authentication to check if the user access token is valid
    and fetch the user from the token and add it to kwargs.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get('HTTP_BEARER')
        user_id = request.META.get('HTTP_USER_ID')
        if not key:
            raise BadRequest(
                'Can not find Bearer token in the request header.')
        if not user_id:
            raise BadRequest(
                'Can not find User-Id in the request header.')

        try:
            user = AccessToken.objects.get(
                key=key, user__id=user_id).user
        except:
            raise UnauthorizedAccess(
                'Invalid Bearer token or User-Id, please re-login.')
        request.user = user
        view.kwargs['user'] = user

        return True
