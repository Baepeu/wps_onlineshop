from django.contrib import admin

from .models import *
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','slug']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','category','name','slug','price','stock','available_display','available_order','created','updated']
    prepopulated_fields = {'slug':('name',)}
    list_editable = ['available_display','available_order','price','stock']

admin.site.register(Product,ProductAdmin)