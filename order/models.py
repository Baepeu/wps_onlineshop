from django.db import models
from shop.models import Product
class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    paid = models.BooleanField(default=False)
    # 결제 시도 전에 주문을 먼저 생성한다.

    class Meta:
        ordering = ['-updated']

    def __str__(self):
        return f"Order {self.id}"

class OrderItem(models.Model):
    # 주문 시스템을 구현할 때는 변동될 수 있는 정보는
    # 항상 별도로 복사해서 저장해둔다.
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='ordered_items')
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order #{self.order.id} item {self.product.name}"

    def get_item_total_price(self):
        return self.price * self.quantity

import uuid
import hashlib
from .iamport import payment_prepare, find_trasaction
class OrderTransactionManager(models.Manager):
    def create_new(self, order, amount, success=None, transaction_status=None):
        if not order:
            raise ValueError("주문이 존재 하지 않습니다.")

        temp_uuid = uuid.uuid1()
        temp_order_id = (str(temp_uuid)+str(order.email)).encode('utf-8')
        hashed_order_id = hashlib.sha1(temp_order_id).hexdigest()[:10]
        merchant_order_id = str(hashed_order_id)
        payment_prepare(merchant_order_id, amount)

        transaction = self.model(
            order=order,
            merchant_order_id=merchant_order_id,
            amount=amount
        )

        if success is not None:
            transaction.success = success
            transaction.transaction_status = transaction_status

        try:
            transaction.save()
        except Exception as e:
            print("save error", e)

            return transaction.merchant_order_id

    def get_transaction(self, merchant_order_id):
        result = find_trasaction(merchant_order_id)
        if result['status'] == 'paid':
            return result
        else:
            return None

class OrderTransaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transaction')
    merchant_order_id = models.CharField(max_length=20, blank=True, null=True)
    transaction_id = models.CharField(max_length=120, blank=True, null=True)
    amount = models.IntegerField(default=0)
    transaction_status = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = OrderTransactionManager()

    def __str__(self):
        return str(self.order.id) + "'s Transaction"

    class Meta:
        ordering = ['-created']













