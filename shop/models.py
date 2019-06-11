from django.db import models
from django.shortcuts import resolve_url
# Create your models here.
# Category - 중첩, 레벨이 있게
from ckeditor_uploader.fields import RichTextUploadingField
class Category(models.Model):
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='sub_categories')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    image = models.ImageField(upload_to='category_images/%Y/%m/%d', blank=True)
    description = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return resolve_url('product_in_category', self.slug)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True)
    image = models.ImageField(upload_to='product_images/%Y/%m/%d')
    description = RichTextUploadingField(blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    available_display = models.BooleanField(default=True)
    available_order = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return "["+self.category.name+"] " + self.name