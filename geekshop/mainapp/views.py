import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from .models import ProductCategory, Product


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_random_product():
    products = Product.objects.filter(is_deleted=False)
    return random.sample(list(products), 1)[0]


def get_same_products(prod):
    same_products = Product.objects\
                            .filter(is_deleted=False, category=prod.category)\
                            .exclude(pk=prod.pk)[:3]
    return same_products


def products_list(request, pk, page=1):

    if pk == 0:
        category = {
            'name': 'все',
            'pk': pk
        }
        products = Product.objects.filter(is_deleted=False).order_by('name')
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = Product.objects.filter(is_deleted=False,
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
        'links_menu': ProductCategory.objects.filter(is_deleted=False),
        'category': category,
        'products': products_paginator,
        'basket': get_basket(request.user),
    }
    return render(request, 'mainapp/products_list.html', content)


def hot_product(request):
    hot_product = get_random_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': 'горячее предложение',
        'links_menu': ProductCategory.objects.exclude(is_deleted=True),
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/hot_product.html', content)


def product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = product.name

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.exclude(is_deleted=True),
        'product': product,
        'basket': get_basket(request.user),
    }

    return render(request, 'mainapp/product.html', content)






