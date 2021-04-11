from django.db import models
from django.contrib.auth import get_user_model
from mainapp.models import Products


class Order(models.Model):
    STATUS_FORMING = 'F'
    STATUS_SENDED = 'S'
    STATUS_PAID = 'P'
    STATUS_MOVING = 'M'
    STATUS_DELAYED = 'D'

    STATUS_CHOICES = (
        (STATUS_FORMING, 'формируется'),
        (STATUS_SENDED, 'отправлен'),
        (STATUS_PAID, 'оплачен'),
        (STATUS_MOVING, 'доставляется'),
        (STATUS_DELAYED, 'отменен'),
    )

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='orders')
    add_dt = models.DateTimeField('время', auto_now_add=True)
    update_dt = models.DateTimeField('время', auto_now=True)
    status = models.CharField('статус', max_length=1,
                              choices=STATUS_CHOICES,
                              default=STATUS_FORMING)
    is_active = models.BooleanField(verbose_name='активен',
                                    default=True)

    class Meta:
        ordering = ('-add_dt',)
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    @property
    def is_forming(self):
        return self.status == self.STATUS_FORMING

    @property
    def total_quantity(self):
        return sum(map(lambda x: x.quantity, self.items.all()))

    @property
    def total_cost(self):
        return sum(map(lambda x: x.product_cost, self.items.all()))


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)

    @property
    def product_cost(self):
        return self.product.price * self.quantity
