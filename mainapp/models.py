from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=256)
    is_active = models.BooleanField(default=True)
    sale = models.FloatField(default=0, validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ])

    def __str__(self):
        return f'{self.name}'


class Products(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=256, blank=True)
    short_description = models.TextField(max_length=256)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='products_images')
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.name}'
