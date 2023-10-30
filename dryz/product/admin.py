from django.contrib import admin

from .models import Product, ProductVariant, ProductImage, ReviewRating


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'selling_price', 'stock', 'category', 'modified_data')
    prepopulated_fields = {'slug': ('product_name',)}


admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(ReviewRating)
