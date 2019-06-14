from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, OrderTransaction
class TransactionInline(admin.TabularInline):
    model = OrderTransaction

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

import csv # csv 파일 생성
import datetime # created, updated - datetime객체인지 여부 확인을 위해, string으로 컨버팅
from django.utils import timezone # 장고에서 사용하는 표준 시각을 반영하기 위핸 모듈
from django.http import HttpResponse # 응답

def export_to_csv(modeladmin, request, queryset):
    # modeladmin - modeladmin.model - 선택된 객체의 모델 정보
    # request - request 정보
    # queryset - 선택된 객체들
    opts = modeladmin.model._meta

    response = HttpResponse(content_type='text/csv')
    current_time =  timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    response['Content-Disposition'] = f'attachment;filename={opts.verbose_name}-{current_time}.csv'
    writer = csv.writer(response)

    # 모델에서 필드 목록 불러오기
    print(opts.get_fields())

    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # 필드명으로 헤더 만들기
    field_headers = [field.verbose_name for field in fields]
    field_headers += ['product name', 'quantity', 'Unit price', 'Total Price']
    writer.writerow(field_headers)

    for obj in queryset:
        data_row = []

        order_items = getattr(obj, 'items').all()
        # 제품 마다 중복 출력될 주문 정보 만들기
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        # 주문 정보와 함께 제품 정보 출력하기
        for order_item in order_items:
            # 주문 정보에 제품 정보를 껴넣기 위해 리스트 복제
            current_data = data_row.copy()
            product_name = order_item.product.name
            current_data.append(product_name)
            current_data.append(order_item.quantity)
            current_data.append(order_item.price)
            current_data.append(order_item.get_item_total_price())
            writer.writerow(current_data)
            # 메모리 확보를 위해 리스트 삭제
            del(current_data)

    return response

export_to_csv.short_description = "Oder Export to CSV"

from django.utils.safestring import mark_safe
from django.shortcuts import resolve_url
def order_detail(obj):
    # 주문 상세 정보 페이
    # 상세 페이지 링크
    url = resolve_url('admin_order_detail', obj.id)
    return mark_safe(f'<a href="{url}">see detail</a>')
order_detail.short_description = 'Detail'

def order_pdf(obj):
    # pdf파일 만들기 뷰로 가는 링크
    url = resolve_url('admin_order_pdf', obj.id)
    return mark_safe(f'<a href="{url}">pdf</a>')
order_pdf.short_description = 'PDF'

class OrderOption(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','paid', order_detail, order_pdf, 'created','updated']
    list_editable = ['paid']
    inlines = [TransactionInline, OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderOption)