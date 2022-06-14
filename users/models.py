from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    code = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username
