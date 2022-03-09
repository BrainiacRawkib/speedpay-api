"""ABSTRACTING DB OPERATIONS FROM VIEWS."""
from apiutils.utils import logger, generate_code
from .constraint_checks import check_category_name, check_product_details
from .models import Category, Product


"""CRUD OPERATIONS"""

"""CREATE"""
def create_category(name):
    try:
        if check_category_name(name=name):
            return None
        return Category.objects.create(name=name)

    except Exception as e:
        logger.error("create_category@Error")
        logger.error(e)
        return None


def create_product(category, title, price, quantity):
    try:
        if check_product_details(title=title):
            return None
        return Product.objects.create(
            code=generate_code('products', 'Product'),
            category=category,
            title=title,
            price=price,
            quantity=quantity

        )

    except Exception as e:
        logger.error("create_product@Error")
        logger.error(e)
        return None

"""RETRIEVE"""
"""UPDATE"""
"""DELETE"""