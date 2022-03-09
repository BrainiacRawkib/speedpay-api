from apiutils.views import http_response
from rest_framework.views import APIView
from .serialiazers import UserSerializer
from .utils import get_user, get_all_users


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        payload = request.data

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
