from apiutils.views import http_response
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from .serialiazers import UserSerializer, LoginSerializer
from .utils import get_user, get_all_users, get_user_access_token


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        payload = request.data
        token = payload['access']

        if not token:
            return http_response(
                'Access Token missing',
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD
            )

        user = get_user_access_token(token)
        serializer = UserSerializer(user)
        return http_response(
            'User retrieved',
            status=status.HTTP_200_OK,
            data=serializer
        )


    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.data
        serializer = LoginSerializer(data=payload)
        if serializer.is_valid():
            error = serializer.validate(payload)
            if not error:
                return http_response(
                    'Login Successful',
                    status=status.HTTP_200_OK,
                    data=serializer.validated_data
                )
        return http_response(
            'Login Failed',
            status=status.HTTP_403_FORBIDDEN,
            data=payload
        )
