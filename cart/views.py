from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.shortcuts import redirect

from shop.models import Product
from .cart import Cart
from .forms import AddToCartForm

@require_POST
def add_product(request, product_id):

    product = Product.objects.filter(pk=product_id)

    if product.exists():
        cart = Cart(request)
        form = AddToCartForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product[0], quantity=cd['quantity'], is_update=cd['is_update'])

    url = request.META['HTTP_REFERER']
    return redirect(url)
