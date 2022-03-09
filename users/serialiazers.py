from apiutils.utils import logger
from rest_framework import serializers
from .models import User
from .utils import create_user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'code', 'first_name', 'last_name', 'username', 'email', 'password', 'contact'
        ]
        read_only_fields = ['code']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        try:
            return create_user(**validated_data), ""

        except Exception as err:
            logger.error('UserSerializer.create@Error')
            logger.error(err)
            return None, str(err)