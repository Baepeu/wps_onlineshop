from django.urls import path

from .views import *
urlpatterns = [
    path('detail/<slug>/', ProductDetail.as_view(), name='product_detail'),
    path('<slug>/', ProductList.as_view(), name='product_in_category'),
    path('', ProductList.as_view(), name='index'),
]