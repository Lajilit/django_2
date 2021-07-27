from django.db import models


class ProductCategory(models.Model):
    objects: models.Manager()
    name = models.CharField(
        verbose_name='наименование',
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True,
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='категория удалена'
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    objects: models.Manager()
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='наименование',
        max_length=128
    )
    image = models.ImageField(
        upload_to='products_images',
        blank=True,
        verbose_name='фото'
    )
    short_desc = models.CharField(
        verbose_name='краткое описание',
        max_length=60,
        blank=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='товар удален'
    )

    class Meta():
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return f"{self.name} ({self.category.name})"
