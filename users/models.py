from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username
