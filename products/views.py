from apiutils.views import http_response, validate_keys
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from users.utils import get_user_access_token
from .serializers import CategorySerializer, ProductSerializer


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CategorySerializer()


    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class ProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        token = request.headers.get('Access-Token')
        if not token:
            return http_response(
                'Access Token missing',
                status=status.HTTP_400_BAD_REQUEST,
                data=ErrorCodes.INVALID_PAYLOAD
            )
        user = get_user_access_token(token)

        if not user:
            return http_response(
                'Session Timed out.',
                status=status.HTTP_408_REQUEST_TIMEOUT
            )


    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass