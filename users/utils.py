"""ABSTRACTING DB OPERATIONS FROM VIEWS."""
from apiutils.utils import logger, generate_code
from rest_framework.authtoken.models import Token
from .constraint_checks import check_user_create_details
from .models import User


"""CRUD OPERATIONS"""

"""CREATE"""
def create_user(first_name, last_name, username, email, password, is_admin=False):
    try:
        if not check_user_create_details(username=username, email=email):
            return None
        user = User.objects.create_user(
            code=generate_code('users', 'User'),
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
            is_admin=is_admin
        )
        token, created = Token.objects.get_or_create(user=user)
        return user, token

    except Exception as e:
        logger.error('create_user@Error')
        logger.error(e)
        return None


"""RETRIEVE"""
def get_user(*args, **kwargs):
    """Retrieve a User by keyword args: username, code, email, or contact"""
    try:
        if kwargs['username']:
            return User.objects.get(username=kwargs['username'])
        elif kwargs['code']:
            return User.objects.get(code=kwargs['code'])
        elif kwargs['email']:
            return User.objects.get(email=kwargs['email'])
        else:
            return None

    except Exception as e:
        logger.error('get_user@Error')
        logger.error(e)
        return None


def get_user_by_access_token(token):
    """Get a user by the access token given."""
    try:
        key = token.split()
        access_token = key[1]
        token = Token.objects.get(key=access_token)
        user = token.user
        if user and user.is_active:
            return user
        return None

    except Exception as e:
        logger.error('get_user_by_access_token@Error')
        logger.error(e)
        return None


def get_all_users():
    try:
        return User.objects.all()

    except Exception as e:
        logger.error('get_all_users@Error')
        logger.error(e)
        return []

"""UPDATE"""

"""DELETE"""

def delete_user(user):
    """Delete a user."""
    try:
        user.is_deleted = True
        user.is_active = False
        user.save()
        return True

    except Exception as e:
        logger.error('delete_user@Error')
        logger.error(e)
        return False
