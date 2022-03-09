"""ABSTRACTING DB OPERATIONS FROM VIEWS."""
from apiutils.utils import logger, generate_code
from rest_framework_simplejwt.tokens import RefreshToken
from .constraint_checks import check_user_create_details
from .models import User


"""CRUD OPERATIONS"""

"""CREATE"""
def create_user(first_name, last_name, username, email):
    try:
        if not check_user_create_details(username=username, email=email):
            return None
        return User.objects.create_user(
            code=generate_code('users', 'User'),
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email
        )

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


"""GET TOKENS FOR AUTHENTICATED USERS"""
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }