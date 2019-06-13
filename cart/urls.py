from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:product_id>/', add_product, name='add_product'),
    path('remove/<int:product_id>/', remove_product, name='remove_product'),
    path('detail/', cart_detail, name='cart_detail'),
]