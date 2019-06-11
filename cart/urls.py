from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:product_id>/', add_product, name='add_product'),
]