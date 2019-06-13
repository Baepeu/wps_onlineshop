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

from django.views.generic.base import View
from django.http import JsonResponse

class OrderCreateAjaxView(View):
    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            data = {
                "order_id":order.id
            }
            return JsonResponse(data)
        return JsonResponse({}, status=401)


class OrderCheckoutAjaxView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({})

class OrderImpAjaxView(View):
    def post(self, request, *args, **kwargs):
        return JsonResponse({})

from .models import Order
def order_complete(request):
    # ajax로 주문 완료시, 완료 페이지로 이동하는 경우에 사용
    order_id = request.GET.get('order_id')
    order = Order.objects.filter(pk=order_id)

    # Todo : 만약 없는 오더 번호일 경우 예외처리
    if order.exists():
        return render(request,'order/order_created.html', {'order':order[0]})









