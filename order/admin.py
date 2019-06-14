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
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    # 필드명으로 헤더 만들기
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime("%Y-%m-%d")
            data_row.append(value)
        writer.writerow(data_row)

    return response

export_to_csv.short_description = "Oder Export to CSV"

from django.utils.safestring import mark_safe
def order_detail(obj):
    # 주문 상세 정보 페이
    # 상세 페이지 링크
    return mark_safe('<a href="#">Detail</a>')
order_detail.short_description = 'Detail'

def order_pdf(obj):
    # pdf파일 만들기 뷰로 가는 링크
    return mark_safe('PDF')
order_pdf.short_description = 'PDF'

class OrderOption(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','paid', order_detail, order_pdf, 'created','updated']
    list_editable = ['paid']
    inlines = [TransactionInline, OrderItemInline]
    actions = [export_to_csv]

admin.site.register(Order, OrderOption)