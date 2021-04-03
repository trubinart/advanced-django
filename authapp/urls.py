from django.urls import path
from authapp.views import  logout, profile
from authapp.views import UserLoginView, UserRegisterView

app_name = 'auth'

urlpatterns = [
   path('login/', UserLoginView.as_view(), name='login'),
   path('register/', UserRegisterView.as_view() , name='register'),
   path('profile/', profile, name='profile'),
   path('logout/', logout, name='logout'),

]