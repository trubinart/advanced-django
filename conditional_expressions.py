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

