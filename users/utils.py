"""ABSTRACTING DB OPERATIONS FROM VIEWS."""
from apiutils.utils import logger, generate_code
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

"""UPDATE"""

"""DELETE"""
