from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apiutils.views import http_response
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from .constraint_checks import check_if_user_is_admin
from .serialiazers import UserSerializer
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
        if not check_if_user_is_admin(user):
            return http_response(
                'You are not authorized to create a user.',
                status=status.HTTP_401_UNAUTHORIZED,
                error_code=ErrorCodes.UNAUTHORIZED
            )
        payload = request.data
        serializer = UserSerializer(data=payload)
        if serializer.is_valid():
            data = serializer.validated_data
            created_user, _ = serializer.create(data)

            if not created_user:
                return http_response(
                    'Internal Server Error.',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code=ErrorCodes.SERVER_ERROR
                )
            return http_response(
                msg="User Successfully Created",
                status=status.HTTP_201_CREATED,
                data=data
            )
        return http_response(
            msg="",
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors,
            error_code=ErrorCodes.GENERIC_ERROR
        )

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class LoginAPIView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        payload = request.data
        context = {'request': request}
        serializer = self.serializer_class(data=payload, context=context)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }
        return http_response(
            'Login Successful',
            status=status.HTTP_200_OK,
            data=data
        )
