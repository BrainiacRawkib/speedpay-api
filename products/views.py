from apiutils.views import http_response, validate_keys
from apiutils.error_codes import ErrorCodes
from rest_framework.views import APIView
from rest_framework import status
from users.constraint_checks import check_if_user_is_admin
from users.utils import get_user_by_access_token
from .serializers import CategorySerializer, ProductSerializer
from .utils import get_all_products, get_categories, get_category, update_product, \
    delete_product, get_product, get_products_by_category


class CategoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query_params = request.query_params
        if query_params:
            category_name = query_params['name']
            category = get_category(category_name)
            if category:
                serializer = CategorySerializer(category)
                return http_response(
                    'Category Retrieved',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            return http_response(
                "Category not found.",
                status=status.HTTP_404_NOT_FOUND
            )
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
        query_params = request.query_params
        if query_params:
            category = get_category(query_params['name'])
            if category:
                products = get_products_by_category(category=category)
                serializer = ProductSerializer(products, many=True)
                return http_response(
                    f'{category} Products retrieved.',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            return http_response(
                f'{category} not found.',
                status=status.HTTP_404_NOT_FOUND,
            )
        products = get_all_products()
        serializer = ProductSerializer(products, many=True)
        return http_response(
            'Products Retrieved.',
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
        serializer = ProductSerializer(data=payload)

        # check for missing keys
        required_keys = ['title', 'category', 'price', 'quantity', 'description']
        missing_keys = validate_keys(payload, required_keys)
        if missing_keys:
            return http_response(
                msg=f"The following key(s) are missing in the request payload: {missing_keys}",
                status=status.HTTP_400_BAD_REQUEST,
                error_code=ErrorCodes.INVALID_PAYLOAD,
            )

        if serializer.is_valid():
            data = serializer.validated_data
            data['category'] = payload['category']['name']
            created_product, _ = serializer.create(data)
            if not created_product:
                return http_response(
                    'Internal Server Error.',
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    error_code=ErrorCodes.SERVER_ERROR,
                    data=serializer.data
                )
            return http_response(
                msg="Product Successfully Created",
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

        query_params = request.query_params

        # check if purchase param is in query parameters
        purchase = query_params['purchase']
        payload = request.data

        serializer = ProductSerializer(data=payload)
        if serializer.is_valid():
            data = serializer.validated_data
            updated_product, _ = update_product(data, user)

            # check if purchase it true to allow user purchase a product
            if purchase == 'true':
                updated_product, _ = update_product(data, user)

                if updated_product:
                    return http_response(
                        'Product Successfully purchased',
                        status=status.HTTP_200_OK,
                        data=serializer.data
                    )
                return http_response(
                    'Error purchasing product',
                    status=status.HTTP_400_BAD_REQUEST
                )
            # if purchase is false, then update the product
            if updated_product:
                return http_response(
                    'Product Successfully updated.',
                    status=status.HTTP_200_OK,
                    data=serializer.data
                )
            return http_response(
                'Error updating product',
                status=status.HTTP_400_BAD_REQUEST
            )
        return http_response(
            msg="",
            status=status.HTTP_400_BAD_REQUEST,
            data=serializer.errors,
            error_code=ErrorCodes.GENERIC_ERROR
        )

    def delete(self, request, *args, **kwargs):
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

        query_params = request.query_params
        product_title = query_params['title']

        if product_title:
            product = get_product(product_title)
            product_to_delete = delete_product(product)
            if product_to_delete:
                return http_response(
                    'Product successfully deleted',
                    status=status.HTTP_204_NO_CONTENT
                )
            return http_response(
                'Error deleting product',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return http_response(
            msg="",
            status=status.HTTP_400_BAD_REQUEST,
            error_code=ErrorCodes.GENERIC_ERROR
        )