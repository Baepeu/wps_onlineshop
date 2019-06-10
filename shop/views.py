from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from .models import *

class ProductList(ListView):
    model = Product
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'slug' in self.kwargs:
            category = Category.objects.filter(slug=self.kwargs['slug'])
            if category.exists():
                queryset = queryset.filter(category=category[0])
            else:
                queryset = queryset.none()
        return queryset