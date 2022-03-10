from apiutils.views import http_response, validate_keys
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from users.constraint_checks import check_if_user_is_admin
from users.utils import get_user_by_access_token
from .serializers import CategorySerializer, ProductSerializer
from .utils import get_all_products, get_categories


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        categories = get_categories()
        serializer = CategorySerializer(categories, many=True)
        return http_response(
            'Categories Retrieved.',
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
        serializer = CategorySerializer(data=payload)

        if serializer.is_valid():
            data = serializer.validated_data
            created_category, _ = serializer.create(data)

            if not created_category:
                return http_response(
                    'Internal Server Error.',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code=ErrorCodes.SERVER_ERROR
                )
            return http_response(
                msg="Category Successfully Created",
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


class ProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass