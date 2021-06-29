from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    objects: models.Manager()
    avatar = models.ImageField(
        upload_to='users_avatars',
        blank=True
    )
    age = models.PositiveIntegerField(
        verbose_name='возраст'
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='пользователь удален'
    )
