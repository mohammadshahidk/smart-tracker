"""Exceptions which used in Apps."""

from rest_framework.exceptions import APIException


# class BaseAPIException(APIException):
#     """ Base API Exception to provide option to fail silently"""
#     send_to_sentry = True
#
#     def __init__(self, *args, **kwargs):
#         if 'send_to_sentry' in kwargs:
#             self.send_to_sentry = kwargs.pop('send_to_sentry')
#         super(BaseAPIException, self).__init__(*args, **kwargs)


class BadRequest(APIException):
    """Request method is invalid."""

    status_code = 400
    default_detail = 'Request details are invalid.'
    default_code = 'bad_request'


class UnauthorizedAccess(APIException):
    """user Authorization failed."""

    status_code = 401
    default_detail = 'User is not authorized to access.'
    default_code = 'unauthorized_access'


class AccessForbidden(APIException):
    """User is not allowed to access."""

    status_code = 403
    default_detail = 'User access is forbidden.'
    default_code = 'access_forbidden'
