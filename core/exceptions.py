from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    ValidationError,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    # 🔐 JWT Errors
    if isinstance(exc, (InvalidToken, TokenError)):
        return Response(
            {
                "success": False,
                "message": "Invalid or expired token",
                "error_code": "AUTH_INVALID_TOKEN",
                "data": None,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # 🔐 Authentication Errors
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {
                "success": False,
                "message": "Authentication failed",
                "error_code": "AUTH_FAILED",
                "data": None,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    if isinstance(exc, NotAuthenticated):
        return Response(
            {
                "success": False,
                "message": "Authentication credentials were not provided",
                "error_code": "AUTH_REQUIRED",
                "data": None,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # 🧾 Validation Errors (IMPORTANT FIX)
    if isinstance(exc, ValidationError):
        return Response(
            {
                "success": False,
                "message": "Validation error",
                "error_code": "VALIDATION_ERROR",
                "data": response.data,  # show actual field errors
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # 🌍 All Other Errors
    if response is not None:
        return Response(
            {
                "success": False,
                "message": str(exc),
                "error_code": "API_ERROR",
                "data": response.data,
            },
            status=response.status_code,
        )

    return response