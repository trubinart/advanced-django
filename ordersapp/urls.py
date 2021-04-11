from django.urls import path
from ordersapp.views import OrderCreate, OrderUpdate, OrderList, FormingComplete

app_name = 'ordersapp'

urlpatterns = [
    path('', OrderList.as_view(), name='index'),
    path('create/', OrderCreate.as_view(), name='create'),
    path('update/<int:pk>', OrderUpdate.as_view(), name='update'),
    path('complete/<int:pk>', FormingComplete.as_view(), name='order_forming_complete'),
]
