from django.db import models
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=256)

    def __str__(self):
        return f'{self.name}'

class Products(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=256, blank=True)
    short_description = models.TextField(max_length=256)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    img = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
        return f'{self.name}'
