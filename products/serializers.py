from apiutils.utils import logger
from rest_framework import serializers
from .models import Category, Product
from .utils import create_category, create_product, update_product


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        try:
            return create_category(validated_data['name']), ""

        except Exception as err:
            logger.error('CategorySerializer.create@Error')
            logger.error(err)
            return None, str(err)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['code', 'category', 'title', 'description', 'price', 'quantity', 'available',
                  'created_at', 'updated_at']
        read_only_fields = ['code', 'created_at', 'updated_at']
        depth = 1

    def create(self, validated_data):
        try:
            return create_product(**validated_data), ""

        except Exception as err:
            logger.error('ProductSerializer.create@Error')
            logger.error(err)
            return None, str(err)

    def update(self, instance, validated_data):
        try:
            return update_product(instance, validated_data), ""

        except Exception as err:
            logger.error('ProductSerializer.update@Error')
            logger.error(err)
            return None, str(err)