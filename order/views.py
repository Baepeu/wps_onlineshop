from django.shortcuts import render

from cart.cart import Cart
from .models import OrderItem
from .forms import OrderForm

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == "POST":
        # 주문 정보가 입력 완료된 상황
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
              #cart.clear()
            return render(request, 'order/order_created.html', {'order': order})
    else:
        form = OrderForm()

    return render(request, 'order/order_create.html', {'form':form})