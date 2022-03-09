from apiutils.views import http_response
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from .serialiazers import UserSerializer
from .utils import get_user, get_all_users


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

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
