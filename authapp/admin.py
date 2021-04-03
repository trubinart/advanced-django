from django.contrib import admin

# Register your models here.

from authapp.models import Users

admin.site.register(Users)