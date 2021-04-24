from django.contrib import admin
from django.urls import path, include, re_path
from mainapp.views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', index, name='main'),
    path('products/', include('mainapp.urls', namespace='products')),
    path('auth/', include('authapp.urls', namespace='auth')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('admin-staff/', include('adminapp.urls', namespace='admin_staff')),
    path('social/', include('social_django.urls', namespace='social')),
    path('orders/', include('ordersapp.urls', namespace='orders')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [re_path(r'^__debug__/', include(debug_toolbar.urls))]