"""ABSTRACTING DB OPERATIONS FROM VIEWS."""
from apiutils.utils import logger, generate_code
from .constraint_checks import check_category_name, check_product_details
from .models import Category, Product


"""CRUD OPERATIONS"""

"""CREATE"""
def create_category(name):
    try:
        if not check_category_name(name):
            return None
        return Category.objects.create(name=name)

    except Exception as e:
        logger.error("create_category@Error")
        logger.error(e)
        return None


def create_product(category, title, price, quantity, description):
    try:
        cat = get_category(category)
        if not check_product_details(title=title):
            return None
        return Product.objects.create(
            code=generate_code('products', 'Product'),
            category=cat,
            title=title,
            price=price,
            quantity=quantity,
            description=description
        )

    except Exception as e:
        logger.error("create_product@Error")
        logger.error(e)
        return None

"""RETRIEVE"""

def get_category(cat_name):
    """Get a specific category."""
    try:
        if cat_name:
            return Category.objects.get(name=cat_name)
        return None

    except Exception as e:
        logger.error('get_category@Error')
        logger.error(e)
        return None


def get_categories():
    """Get all categories."""
    try:
        return Category.objects.all()

    except Exception as e:
        logger.error('get_categories@Error')
        logger.error(e)
        return []


def get_product(title):
    """Get product by title or code."""
    try:
        if title:
            product = Product.objects.get(title=title)
            if product.available:
                return product
        return None

    except Exception as e:
        logger.error('get_product@Error')
        logger.error(e)
        return None


def get_all_products():
    """Get all available products."""
    try:
        return Product.objects.filter(available=True)

    except Exception as e:
        logger.error('get_all_products@Error')
        logger.error(e)
        return []


def get_products_by_category(category=None):
    """Get products by specified category."""
    try:
        if category:
            return get_all_products().filter(category=category)
        return get_all_products()

    except Exception as e:
        logger.error('get_products_by_category@Error')
        logger.error(e)
        return []


"""UPDATE"""

def update_product(product, validated_data, user=None):
    """Update a product."""
    try:
        if user:
            product.quantity -= validated_data.get('quantity', None)
            product.user = user
            product.save()
            return product
        product.price = validated_data.get('price', product.price)
        product.quantity = validated_data.get('quantity', product.quantity)
        product.description = validated_data.get('description', product.description)
        product.save()
        return product

    except Exception as e:
        logger.error('update_product@Error')
        logger.error(e)
        return None


"""DELETE"""

def delete_product(product):
    """Delete a product. Set a product available=False to delete the product."""
    try:
        product.available = False
        product.save()
        return True

    except Exception as e:
        logger.error('delete_product@Error')
        logger.error(e)
        return False