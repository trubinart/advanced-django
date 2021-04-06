from django.urls import path
from authapp.views import logout, profile, login, register, verify

app_name = 'auth'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<str:activation_key>', verify, name='verify'),

]
