from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from .models import *

class ProductList(ListView):
    model = Product
    template_name = 'shop/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        categories = Category.objects.filter(parent_category=Category.objects.get(pk=1)).order_by('name')
        kwargs.update({'categories':categories})
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if 'slug' in self.kwargs:
            category = Category.objects.filter(slug=self.kwargs['slug'])
            if category.exists():
                queryset = queryset.filter(category=category[0])
            else:
                queryset = queryset.none()
        return queryset