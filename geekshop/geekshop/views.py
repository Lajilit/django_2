from django.shortcuts import render
from mainapp.models import Product
from mainapp.views import get_basket


def index(request):

    data = {
        'title': 'магазин',
        'products': Product.objects.exclude(is_deleted=True)[:4],
        'basket': get_basket(request.user),
    }
    return render(request, 'index.html', context=data)


def contact(request):
    data = {
        'title': 'наши контакты',
        'basket': get_basket(request.user),
    }
    return render(request, 'contact.html', context=data)
