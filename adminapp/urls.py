from django.urls import path
from adminapp import views

app_name = 'adminapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('read/', views.UsersListView.as_view(), name='read'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='delete'),
]