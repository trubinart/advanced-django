from django.urls import path
from ordersapp.views import OrderCreate, OrderUpdate, OrderList, order_forming_complete, \
                            OrderDetail, OrderDelete
app_name = 'ordersapp'

urlpatterns = [
    path('', OrderList.as_view(), name='index'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('complete/<int:pk>', order_forming_complete, name='order_forming_complete'),
    path('read/<int:pk>', OrderDetail.as_view(), name='read'),
    path('delete/<int:pk>', OrderDelete.as_view(), name='delete'),
]
