from django.contrib import admin

from .models import Category, Sub_Category


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description', 'is_visible', 'cat_image',)
    prepopulated_fields = {'slug': ('category_name',)}


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('sub_category_name','category', 'description', 'is_visible', 'cat_image',)
    prepopulated_fields = {'slug': ('sub_category_name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Sub_Category,SubCategoryAdmin)
