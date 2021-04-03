from django.contrib import admin

# Register your models here.
# login - admin / password - admin
from mainapp.models import Category, Products

admin.site.register(Category)
admin.site.register(Products)