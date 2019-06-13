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
    print(cart.cart.values())
    return redirect('cart_detail')

def remove_product(request, product_id):
    product = Product.objects.filter(pk=product_id)
    if product.exists():
        cart = Cart(request)
        cart.remove(product[0])
    return redirect('cart_detail')

# Todo : Cart Detail View
def cart_detail(request):
    # 장바구니에 담겨 있는 제품 목록 띄우기, 제품 수량 수정, 지우기, 장바구니 비우기 버튼 구현
    cart = Cart(request)
    for item in cart:
        item['quantity_form'] = AddToCartForm(initial={'quantity':item['quantity'], 'is_update':True})

    continue_url = '/'
    # 현재 페이지 주소 얻기
    # 1) request.build_absolute_uri('?') : 쿼리스트링 없이
    # 2) request.build_absolute_uri() : 쿼리스트링까지 얻어오기
    current_url = request.build_absolute_uri('?')
    if 'HTTP_REFERER' in request.META and current_url != request.META['HTTP_REFERER']:
        continue_url = request.META['HTTP_REFERER']

    return render(request,'cart/cart_detail.html', {'cart':cart, 'continue_url':continue_url})
