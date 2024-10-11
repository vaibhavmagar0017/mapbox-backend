from src.base.error_conf import ErrorConfig
from src.base.enums import ResponseTypeEnum
from fastapi import status

from src import constants

# Authorization App related messages
ErrorConfig.extend(
    {
        constants.USER_TOKEN_EXPIRED: {
            "response_code": constants.USER_TOKEN_EXPIRED,
            "http_code": status.HTTP_401_UNAUTHORIZED,
            "response_type": ResponseTypeEnum.error,
            "message": "User token expired",
        },
        constants.USER_TOKEN_ERROR: {
            "response_code": constants.USER_TOKEN_ERROR,
            "http_code": status.HTTP_401_UNAUTHORIZED,
            "response_type": ResponseTypeEnum.error,
            "message": "User token is not valid",
        },
        constants.USER_TOKEN_INVALID: {
            "response_code": constants.USER_TOKEN_INVALID,
            "http_code": status.HTTP_401_UNAUTHORIZED,
            "response_type": ResponseTypeEnum.error,
            "message": "User token is not valid",
        },
        constants.AUTHORIZATION_REQUIRED: {
            "response_code": constants.AUTHORIZATION_REQUIRED,
            "http_code": status.HTTP_401_UNAUTHORIZED,
            "response_type": ResponseTypeEnum.error,
            "message": "Authorization is required for this action",
        },
        constants.USER_NOT_REGISTERED: {
            "response_code": constants.USER_NOT_REGISTERED,
            "http_code": status.HTTP_404_NOT_FOUND,
            "response_type": ResponseTypeEnum.error,
            "message": "User is not registered.",
        },

        constants.HTTP_409_CONFLICT: {
            "response_code": constants.HTTP_409_CONFLICT,
            "http_code": status.HTTP_409_CONFLICT,
            "response_type": ResponseTypeEnum.error,
            "message": "Record already exists",
        },
    }
)
