"""ABSTRACTING DB OPERATIONS FROM VIEWS."""
from apiutils.utils import logger, generate_code
from .models import Category, Product


"""CRUD OPERATIONS"""

"""CREATE"""
def create_category(name):
    try:
        return Category.objects.create(name=name)

    except Exception as e:
        logger.error("create_category@Error")
        logger.error(e)
        return None


def create_product(name):
    try:
        pass

    except Exception as e:
        logger.error("create_product@Error")
        logger.error(e)
        return None

"""RETRIEVE"""
"""UPDATE"""
"""DELETE"""