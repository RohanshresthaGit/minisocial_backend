from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from .exceptions import ApiException

def custom_exception_handler(exc, context):

    if isinstance(exc, ApiException):
        return Response({
            "isSuccess": False,
            "responseMsg": str(exc.detail),
            "status_code": exc.status_code
        }, status = exc.status_code)
    
    response = exception_handler(exc, context)

    if response is not None:
        message = None

        if isinstance(response.data, dict):
            message = list(response.data.values())[0]
            if isinstance(message, list):
                message = message[0]
        else:
            message = str(response.data)

        return Response({
            "isSuccess": False,
            "responseMsg": message,
            "status_code": response.status_code
        }, status = response.status_code)
    
    return Response({
        "isSuccess": False,
        "responseMsg": "An unexpected error occurred.",
        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
    }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    