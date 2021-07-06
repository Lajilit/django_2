from django.shortcuts import render
from mainapp.models import Product


def index(request):
    data = {
        'title': 'магазин',
        'products': Product.objects.exclude(is_deleted=True)[:4],
    }
    return render(request, 'index.html', context=data)


def contact(request):
    data = {
        'title': 'наши контакты',
    }
    return render(request, 'contact.html', context=data)
