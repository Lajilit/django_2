import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
from django.conf import settings
from django.core.cache import cache

def get_links_menu():
    if settings.LOW_CACHE:
        key = "links_menu"
        links_menu = cache.get(key)
        if links_menu is None:
            # print(f'caching {key}')
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f"category_{pk}"
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = "products"
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                is_active=True,
                category__is_active=True
            ).select_related("category")
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(
            is_active=True,
            category__is_active=True
        ).select_related("category")


def get_product(pk):
    if settings.LOW_CACHE:
        key = f"product_{pk}"
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = "products_orederd_by_price"
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                is_active=True,
                category__is_active=True
            ).order_by("price")
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(
            is_active=True,
            category__is_active=True
        ).order_by("price")


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f"products_in_category_orederd_by_price_{pk}"
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True,
                category__is_active=True
            ).order_by(
                "price"
            )
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(
            category__pk=pk,
            is_active=True,
            category__is_active=True
        ).order_by("price")

def index(request):
    products = get_products().order_by('-id')[:4]
    data = {
        'title': 'магазин',
        'products': products,
    }
    return render(request, 'mainapp/index.html', context=data)


def contact(request):
    data = {
        'title': 'наши контакты',
    }
    return render(request, 'mainapp/contact.html', context=data)


def get_random_product():
    products = get_products()
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
        products = get_products_orederd_by_price()
    else:
        category = get_category(pk)
        products = get_products_in_category_orederd_by_price(pk)
    paginator = Paginator(products, 4)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': 'продукты',
        'links_menu': get_links_menu(),
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
    product = get_product(pk)
    title = product.name

    content = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': product,
    }

    return render(request, 'mainapp/product.html', content)
