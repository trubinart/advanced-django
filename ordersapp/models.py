from django.db import models
from django.contrib.auth import get_user_model
from mainapp.models import Products
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete


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

    def delete(self, using=None, keep_parents=False):
        print('Order delete')
        self.items.delete()
        super().delete()


class OrderItemManager(models.QuerySet):
    def delete(self):
        print('QS deleet')
        super(OrderItemManager, self).delete()


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('количество', default=0)

    objects = OrderItemManager.as_manager()

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @classmethod
    def get_item(cls, pk):
        return cls.objects.filter(pk=pk).first()


@receiver(pre_save, sender=OrderItem)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    print('orderitem save2')
    if instance.pk:
        instance.product.quantity += sender.get_item(instance.pk).quantity - \
                                     instance.quantity

    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=OrderItem)
def product_quantity_update_delete(sender, instance, **kwargs):
    print('orderitem delete2')
    instance.product.quantity += instance.quantity
    instance.product.save()
