from shop.models import Category

def category(request):
    categories = Category.objects.filter(parent_category=Category.objects.get(pk=1)).order_by('name')
    return {'categories':categories}