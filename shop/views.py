from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView

from .models import *

class ProductList(ListView):
    model = Product
    template_name = 'shop/product_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        # pk = 1 : Home
        categories = Category.objects.filter(parent_category=Category.objects.get(pk=1)).order_by('name')
        kwargs.update({'categories':categories})
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        # 상위 카테고리를 고르면 하위 카테고리 제품들이 한꺼번에 출력되도록 변경
        queryset = super().get_queryset()
        if 'slug' in self.kwargs:
            category = Category.objects.filter(slug=self.kwargs['slug'])
            if category.exists():
                category |= self.get_category_list(category[0])
                queryset = queryset.filter(category__in=category)
            else:
                queryset = queryset.none()
        return queryset

    def get_category_list(self,category):
        categories = category.sub_categories.all()
        for category in categories:
            categories |= self.get_category_list(category)
        return categories