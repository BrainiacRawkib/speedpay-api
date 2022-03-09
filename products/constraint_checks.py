"""DATABASE UNIQUE CONSTRAINT CHECKS"""
from apiutils.utils import logger
from .models import Category, Product


def check_category_name(name):
    try:
        if Category.objects.filter(name=name).exists():
            return False
        return True

    except Exception as e:
        logger.error('check_category_name@Error')
        logger.error(e)
        return False


def check_product_details(code, title):
    try:
        if Product.objects.filter(code=code).exists():
            return False
        if Product.objects.filter(title=title).exists():
            return False
        return True

    except Exception as e:
        logger.error('check_product_details@Error')
        logger.error(e)
        return None