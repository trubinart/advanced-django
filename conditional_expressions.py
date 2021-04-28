import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geekshop.settings')
import django

django.setup()

from django.db.models import F, Q, When, Case, DecimalField, IntegerField
from mainapp.models import Products, Category
from django.db import connection
from mainapp.views import db_profile_by_type

# activ_closes = Products.objects.filter(Q(category__name='Одежда') & Q(category__is_active=True))
# print(activ_closes)
# db_profile_by_type('conditional_expressions', '', connection.queries)

sale_under_3000 = 0.1
sale_3000_5000 = 0.2
sale_above_5000 = 0.3

product_under_3000 = Q(price__lte=3000)
product_3000_5000 = Q(price__gte=3000, price__lte=5000)
product_above_5000 = Q(price__gte=5000)

product_under_3000_when = When(product_under_3000, then=3)
product_3000_5000_when = When(product_3000_5000, then=5)
product_above_5000_when = When(product_above_5000, then=7)

product_sale_price_under_3000 = When(product_under_3000, then=F('price') * sale_under_3000)
product_sale_price_3000_5000 = When(product_3000_5000, then=F('price') * sale_3000_5000)
product_sale_price_above_5000 = When(product_above_5000, then=F('price') * sale_above_5000)

sale_products = Products.objects.annotate(
    choise_sale=Case(
        product_under_3000_when,
        product_3000_5000_when,
        product_above_5000_when,
        output_field=IntegerField(),
    )
).annotate(
    sale_price=Case(
        product_sale_price_under_3000,
        product_sale_price_3000_5000,
        product_sale_price_above_5000,
        output_field=IntegerField(),
    )
).order_by('sale_price')

for orderitem in sale_products:
   print(f'{orderitem.name} - {orderitem.choise_sale} - {orderitem.sale_price}')
