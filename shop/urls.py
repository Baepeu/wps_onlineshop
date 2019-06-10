from django.urls import path

from .views import *
urlpatterns = [
    path('<slug>/', ProductList.as_view(), name='product_in_category'),
    path('', ProductList.as_view(), name='index'),
]