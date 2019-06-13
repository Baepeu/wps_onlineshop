from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderOption(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','paid','created','updated']
    inlines = [OrderItemInline]
admin.site.register(Order, OrderOption)