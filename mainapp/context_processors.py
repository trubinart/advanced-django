from mainapp.models import Category
from django.core.cache import cache
from django.conf import settings


def categories(request):
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if not categories:
            categories = Category.objects.all()
            cache.set(key, categories)
        return {
            'categories': categories,
        }
    else:
        return {
            'categories': Category.objects.all(),
        }


