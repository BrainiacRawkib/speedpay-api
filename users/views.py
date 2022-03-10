from apiutils.views import http_response
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from .serialiazers import UserSerializer, LoginSerializer
from .utils import get_user, get_all_users, get_user_by_access_token


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return http_response(
                'Bad Request. Access Token missing.',
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_user_by_access_token(token)
        if user is None:
            return http_response(
                msg="Your session has expired. Please login.",
                status=status.HTTP_401_UNAUTHORIZED,
                error_code=ErrorCodes.UNAUTHENTICATED
            )

        users = get_all_users()
        serializer = UserSerializer(users, many=True)
        query_params = request.query_params
        if query_params:
            username = query_params['username']
            if username:
                user = get_user(username)
                if user:
                    serializer = UserSerializer(user)
                    return http_response(
                        'User Retrieved',
                        status=status.HTTP_200_OK,
                        data=serializer.data
                    )
                return http_response(
                    'User not found',
                    status=status.HTTP_404_NOT_FOUND,
                )
        return http_response(
            'Users Retrieved',
            status=status.HTTP_200_OK,
            data=serializer.data
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
            return http_response(
                'Login Successful',
                status=status.HTTP_200_OK,
                data=payload
            )
