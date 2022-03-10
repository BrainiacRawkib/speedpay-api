from django.db import models
from django.utils.timezone import now
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, related_name='products', on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
