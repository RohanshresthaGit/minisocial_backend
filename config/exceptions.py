from rest_framework.exceptions import APIException
from rest_framework import status

class ApiException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Something went wrong."
    initializer = False

    def __init__(self, message= None, status_code=None):
        if message is not None:
            self.detail = message
        if status_code is not None:
            self.status_code = status_code

class NotFoundException(ApiException):
    def __init__(self, message="Not Found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class BadRequestException(ApiException):
    def __init__(self, message="Bad Request"):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)

class unauthorizedException(ApiException):
    def __init__(self, message="Unauthorized"):
        super().__init(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class ForbiddenException(ApiException):
    def __init__(self, message= "Forbidden"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)

class InternalServerErrorException(ApiException):
    def __init__(self, message= "Internal Server Error"):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)