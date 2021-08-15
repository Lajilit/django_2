from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    objects: models.Manager()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='basket')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество',
                                           default=0)
    add_datetime = models.DateTimeField(verbose_name='время',
                                        auto_now_add=True)

    @property
    def product_cost(self):
        """return cost of all products this type"""
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(id=pk)

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user)