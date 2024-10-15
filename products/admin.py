from django.contrib import admin
from .models import Brand, Product, Category, Tag

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'image',
    )
    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class BrandAmin(admin.ModelAdmin):
    list_display = (
        'brand',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_tag',
        'tag',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAmin)
admin.site.register(Tag, TagAdmin)
