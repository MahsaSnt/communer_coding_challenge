from rest_framework import status
from rest_framework.exceptions import APIException


class AssigneesUsernamesTypeException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'it should be tuple or list.'


class NotExistingDeveloperException(APIException):
    def __init__(self, username_list):
        self.detail = f'no developer with {", ".join(username_list)} username.'
        self.status_code = status.HTTP_400_BAD_REQUEST

