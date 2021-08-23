import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product



def index(request):
    data = {
        'title': 'магазин',
        'products': Product.objects.filter(is_active=True).order_by('-id')[:4],
    }
    return render(request, 'mainapp/index.html', context=data)


def contact(request):
    data = {
        'title': 'наши контакты',
    }
    return render(request, 'mainapp/contact.html', context=data)


def get_random_product():
    products = Product.objects.filter(is_active=True)
    return random.sample(list(products), 1)[0]


def get_same_products(prod):
    same_products = Product.objects \
                        .filter(is_active=True, category=prod.category) \
                        .exclude(pk=prod.pk)[:3]
    return same_products


def products_list(request, pk, page=1):
    if pk == 0:
        category = {
            'name': 'все',
            'pk': pk
        }
        products = Product.objects.filter(is_active=True).order_by('name')
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(is_active=True,
                                          category__pk=pk).order_by('name')
    paginator = Paginator(products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': 'продукты',
        'links_menu': ProductCategory.objects.filter(is_active=True),
        'category': category,
        'products': products_paginator,
    }
    return render(request, 'mainapp/products_list.html', content)


def hot_product(request):
    hot_product = get_random_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'горячее предложение',
        'links_menu': ProductCategory.objects.filter(is_active=True),
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/hot_product.html', content)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = product.name

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.filter(is_active=True),
        'product': product,
    }

    return render(request, 'mainapp/product.html', content)
