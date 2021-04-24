from django.shortcuts import render
import json
from django.http import JsonResponse
import datetime
from mainapp.models import Category, Products
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings


# Create your views here.
def index(request):
    dateTime = datetime.datetime.now()
    content = {
        'title': 'GeekShop Store',
        'h1': 'GeekShop Store',
        'date': dateTime
    }
    return render(request, 'mainapp/index.html', content)


# def products(request, category_id=None):
#     content = {a
#         'title': 'GeekShop - Каталог',
#         'h1': 'GeekShop',
#         'products': Products.objects.filter(category_id=category_id) if category_id else Products.objects.all(),
#         'categories': Category.objects.all(),
#     }
#     return render(request,'mainapp/products.html', content)



def products(request, category_id=None, page=1):
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Products.objects.all()
            cache.set(key, products)
    else:
        if category_id:
            products = Products.objects.filter(category_id=category_id)
        else:
            products = Products.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': 'GeekShop - Каталог',
        'h1': 'GeekShop',
        'products': products_paginator,
    }
    return render(request, 'mainapp/products.html', content)


def price(request, pk):
    if request.is_ajax():
        product = Products.objects.filter(pk=pk).first()
        print(product)
        return JsonResponse(
            {'price': product and product.price or 0}
        )