from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Q

from adminapp.views import db_profile_by_type
from mainapp.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_products = Product.objects.filter(Q(category__id=1) | Q(category__id=2)).select_related()
        print(len(test_products))
        print(test_products.count())
        print(test_products)
        db_profile_by_type("learn db", "", connection.queries)