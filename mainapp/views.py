from django.shortcuts import render
import json
from django.http import JsonResponse
import datetime
from mainapp.models import Category, Products
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.db.models import F

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


def db_profile_by_type(sender, q_type, queries):
    print(f'db profile {q_type} for {sender}:')
    for query in filter(lambda x: q_type in x, map(lambda x: x['sql'], queries)):
        print(query)


@receiver(pre_save, sender=Category)
def update_prod_cat_save(sender, instance, **kwargs):
    print(instance)
    print(instance.products_set)
    if instance.pk:
        if instance.is_active:
            instance.products_set.update(is_active=True)
        else:
            instance.products_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)

@receiver(pre_save, sender=Category)
def update_prod_cat_save(sender, instance, **kwargs):
    if instance.sale > 0:
        instance.products_set.update(price=F('price') * (1-instance.sale))
        db_profile_by_type(sender, 'UPDATE', connection.queries)