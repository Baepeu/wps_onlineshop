from django.urls import path

from .views import *
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('order_complete/', order_complete, name='order_complete'),
]