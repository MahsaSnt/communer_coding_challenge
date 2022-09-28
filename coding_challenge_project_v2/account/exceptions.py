from rest_framework import status
from rest_framework.exceptions import APIException


class NotSamePassword2Exception(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'password2 is not as same as password.'


class ExistingUsernameException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'this username already exists.'
