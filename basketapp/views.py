from django.shortcuts import render
from mainapp.models import Products
from basketapp.models import Basket
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse

@login_required
def basket_add(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    baskets = Basket.objects.all().filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def basket_edit(request, name, quantity):
    if request.is_ajax():
        quantity_2 = int(quantity)
        new_basket = Basket.objects.get(id=int(name))

        if quantity_2 > 0:
            new_basket.quantity = quantity_2
            new_basket.save()
        else:
            new_basket.delete()

    basket_final = Basket.objects.filter(user=request.user)

    content = {
        'baskets': basket_final
    }

    result = render_to_string('basketapp/basket.html', content)

    return JsonResponse({'result': result})