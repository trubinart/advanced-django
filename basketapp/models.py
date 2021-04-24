from django.db import models
from django.conf import settings
from django.utils.functional import cached_property

from mainapp.models import Products
from authapp.models import Users


class Basket(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.user} от {self.created_timestamp}"

    def sum(self):
        return self.quantity * self.product.price

    @cached_property
    def get_items_cached(self):
        return Basket.objects.filter(user=self.user).select_related()

    def total_quantity(self):
        baskets = self.get_items_cached
        return sum(basket.quantity for basket in baskets)

    def total_sum(self):
        baskets = self.get_items_cached
        return sum(basket.sum() for basket in baskets)


